"""Native multi-GPU two-sided MoE communication, including empty origins.

Launch from the shared CLI, without torchrun. Each CUDA-event sample measures
one eager dispatch or combine, excluding simulated expert work. CSV median_time
is the maximum rank median combine latency in milliseconds, per schedule stage;
std_time belongs to that same rank. Raw per-rank samples are retained as JSON.
"""

import argparse
import json
import math
import statistics
import tempfile
from datetime import timedelta
from pathlib import Path


def token_schedule(text, ep_size, capacity):
    try:
        stages = [
            [int(count) for count in stage.split(",")] for stage in text.split(";")
        ]
    except ValueError as error:
        raise ValueError(
            "Use comma-separated ranks and semicolon-separated stages"
        ) from error
    for counts in stages:
        if len(counts) != ep_size or min(counts) < 0 or not 0 < max(counts) <= capacity:
            raise ValueError(
                "Each stage needs ep_size nonnegative counts and a positive maximum <= capacity"
            )
    return stages


def parse_moe_ep_comm_args(line, parser):
    parser.add_argument("--backend", choices=["nvlink_two_sided"], required=True)
    parser.add_argument("--ep_size", type=int, required=True)
    parser.add_argument("--rank_token_schedule", required=True)
    parser.add_argument("--hidden_size", type=int, required=True)
    parser.add_argument("--top_k", type=int, required=True)
    parser.add_argument("--num_experts", type=int, required=True)
    parser.add_argument("--quant", choices=["bf16"], required=True)
    parser.add_argument("--expert_output_ndim", type=int, choices=[2, 3], required=True)
    parser.add_argument(
        "--output_mode", choices=["allocate", "provided"], required=True
    )
    parser.add_argument("--max_num_tokens_per_rank", type=int, required=True)
    parser.add_argument(
        "--warmup", dest="dry_run_iters", type=int, default=argparse.SUPPRESS
    )
    parser.add_argument(
        "--iters", dest="num_iters", type=int, default=argparse.SUPPRESS
    )
    parser.add_argument("--perfect_router", action="store_true", required=True)
    parser.add_argument("--iter_stats", action="store_true", required=True)
    parser.add_argument("--output_file", required=True)
    args = parser.parse_args(line)
    if (
        args.ep_size < 2
        or args.hidden_size <= 0
        or args.hidden_size % 8
        or args.num_experts <= 0
        or args.num_experts % 4
        or args.num_experts % args.ep_size
        or not 1 <= args.top_k <= min(32, args.num_experts)
        or args.top_k < args.ep_size
        or args.max_num_tokens_per_rank <= 0
        or args.dry_run_iters <= 0
        or args.num_iters < 2
        or not args.no_cuda_graph
        or not args.refcheck
        or args.allow_output_mismatch
        or not args.case_tag
    ):
        parser.error(
            "Invalid two-sided shape, iterations, or missing --no_cuda_graph/--refcheck/case_tag"
        )
    try:
        token_schedule(
            args.rank_token_schedule, args.ep_size, args.max_num_tokens_per_rank
        )
    except ValueError as error:
        parser.error(str(error))
    return args


def report_rows(reports, args):
    stages = token_schedule(
        args.rank_token_schedule, args.ep_size, args.max_num_tokens_per_rank
    )
    if len(reports) != args.ep_size or sorted(
        report["rank"] for report in reports
    ) != list(range(args.ep_size)):
        raise ValueError("Missing or duplicate EP rank reports")
    identity = (
        "case_tag",
        "backend",
        "ep_size",
        "rank_token_schedule",
        "hidden_size",
        "top_k",
        "num_experts",
        "quant",
        "expert_output_ndim",
        "output_mode",
        "max_num_tokens_per_rank",
        "num_iters",
        "dry_run_iters",
        "random_seed",
    )
    for report in reports:
        if any(report["configuration"][key] != getattr(args, key) for key in identity):
            raise ValueError("Rank report configuration mismatch")
        if len(report["stages"]) != len(stages):
            raise ValueError("Incomplete schedule report")
    rows = []
    for stage_index, counts in enumerate(stages):
        phase_stats = {"dispatch": [], "combine": []}
        for report in reports:
            stage = report["stages"][stage_index]
            if (
                stage["counts"] != counts
                or stage["preflight"] is not True
                or stage["postflight"] is not True
            ):
                raise ValueError("Missing correctness gate or wrong stage")
            if counts[report["rank"]] == 0 and stage["valid_received_rows"] <= 0:
                raise ValueError("Empty origin did not serve remote work")
            if stage["return_collective_calls"] != 1:
                raise ValueError("Return collective was not executed exactly once")
            for phase, values in phase_stats.items():
                samples = stage[phase + "_ms"]
                if len(samples) != args.num_iters or any(
                    not math.isfinite(sample) or sample <= 0 for sample in samples
                ):
                    raise ValueError(
                        "Missing, non-finite, or non-positive latency samples"
                    )
                values.append(
                    (
                        statistics.median(samples),
                        statistics.pstdev(samples),
                        report["rank"],
                    )
                )
        combine_median, combine_std, measured_rank = max(phase_stats["combine"])
        dispatch_median, dispatch_std, _ = max(phase_stats["dispatch"])
        rows.append(
            {
                **{key: getattr(args, key) for key in identity},
                "routine": args.routine,
                "median_time": combine_median,
                "std_time": combine_std,
                "dispatch_median_time": dispatch_median,
                "dispatch_std_time": dispatch_std,
                "schedule_stage": stage_index,
                "measurement_rank": measured_rank,
                "timing_metric": "max_rank_median_combine_cuda_event_ms",
                "input_dtype": "bfloat16",
                "refcheck_passed": True,
                "no_cuda_graph": True,
                "use_cupti": False,
            }
        )
    return rows


def _dispatch(comm, inputs, counts):
    hidden, ids, weights = inputs
    return comm.dispatch(hidden, ids, weights, runtime_max_tokens_per_rank=max(counts))


def _checked_round(comm, inputs, counts, output, args, rank):
    import torch

    received = _dispatch(comm, inputs, counts)
    ids = received.topk_ids.long()
    first_local = rank * comm.num_local_experts
    is_local = (ids >= first_local) & (ids < first_local + comm.num_local_experts)
    valid = is_local.any(-1, keepdim=True)
    scale = torch.where(
        is_local, received.topk_weights.float() * (ids + 1).float(), 0
    ).sum(-1, keepdim=True)
    expert = torch.where(valid, received.hidden_states.float() * scale, 0).to(
        torch.bfloat16
    )
    if args.expert_output_ndim == 3:
        expert = expert.view(args.ep_size, max(counts), args.hidden_size)
    return_calls = 0
    original = comm._alltoallv

    def counted_return(*call_args, **call_kwargs):
        nonlocal return_calls
        return_calls += 1
        return original(*call_args, **call_kwargs)

    comm._alltoallv = counted_return
    try:
        combined = (
            comm.combine(expert)
            if output is None
            else comm.combine(expert, output=output)
        )
    finally:
        comm._alltoallv = original
    hidden, ids, weights = inputs
    reference = hidden.float() * (weights * (ids.long() + 1).float()).sum(
        -1, keepdim=True
    )
    torch.testing.assert_close(combined.float(), reference, rtol=2e-2, atol=5e-2)
    assert (
        combined.shape == hidden.shape
        and combined.dtype == hidden.dtype
        and combined.device == hidden.device
    )
    assert output is None or combined is output
    valid_rows = int(valid.sum().item())
    assert counts[rank] != 0 or valid_rows > 0
    assert return_calls == 1
    return expert, valid_rows, return_calls


def _rank_worker(rank, args, directory):
    import torch
    import torch.distributed as dist

    from flashinfer.moe_ep import (
        BootstrapConfig,
        MoEEpCommParams,
        NVLinkTwoSidedConfig,
        create_communication,
    )
    from moe_ep.moe_ep_bench_utils import make_routing

    torch.set_num_threads(1)
    torch.cuda.set_device(rank)
    torch.manual_seed(args.random_seed + rank)
    device = torch.device("cuda", rank)
    directory = Path(directory)
    dist.init_process_group(
        "nccl",
        init_method=(directory / "rendezvous").as_uri(),
        rank=rank,
        world_size=args.ep_size,
        timeout=timedelta(minutes=2),
    )
    comm = None
    try:
        comm = create_communication(
            BootstrapConfig(world_size=args.ep_size, rank=rank, device=rank),
            MoEEpCommParams(
                num_experts=args.num_experts,
                top_k=args.top_k,
                max_tokens_per_rank=args.max_num_tokens_per_rank,
                hidden_size=args.hidden_size,
            ),
            NVLinkTwoSidedConfig(),
        )
        stages = token_schedule(
            args.rank_token_schedule, args.ep_size, args.max_num_tokens_per_rank
        )
        prepared = []
        records = []
        for counts in stages:
            hidden = torch.randn(
                counts[rank], args.hidden_size, dtype=torch.bfloat16, device=device
            )
            ids, weights = make_routing(
                counts[rank], args.top_k, args.num_experts, args.ep_size, True, device
            )
            inputs = (hidden, ids, weights)
            output = (
                torch.empty_like(hidden) if args.output_mode == "provided" else None
            )
            expert, valid_rows, calls = _checked_round(
                comm, inputs, counts, output, args, rank
            )
            expert.zero_()
            prepared.append((inputs, expert, output))
            records.append(
                dict(
                    counts=counts,
                    preflight=True,
                    postflight=False,
                    valid_received_rows=valid_rows,
                    return_collective_calls=calls,
                    dispatch_ms=[],
                    combine_ms=[],
                )
            )
        events = [torch.cuda.Event(enable_timing=True) for _ in range(4)]
        for iteration in range(args.dry_run_iters + args.num_iters):
            for stage_index, counts in enumerate(stages):
                inputs, expert, output = prepared[stage_index]
                dist.barrier()
                torch.cuda.synchronize()
                events[0].record()
                _dispatch(comm, inputs, counts)
                events[1].record()
                events[2].record()
                if output is None:
                    comm.combine(expert)
                else:
                    comm.combine(expert, output=output)
                events[3].record()
                torch.cuda.synchronize()
                if iteration >= args.dry_run_iters:
                    records[stage_index]["dispatch_ms"].append(
                        events[0].elapsed_time(events[1])
                    )
                    records[stage_index]["combine_ms"].append(
                        events[2].elapsed_time(events[3])
                    )
        for stage_index, counts in enumerate(stages):
            inputs, _, output = prepared[stage_index]
            _checked_round(comm, inputs, counts, output, args, rank)
            records[stage_index]["postflight"] = True
        torch.cuda.synchronize()
        dist.barrier()
        for record in records:
            for phase in ("dispatch", "combine"):
                samples = record[phase + "_ms"]
                record[phase + "_stats_ms"] = dict(
                    median=statistics.median(samples),
                    mean=statistics.mean(samples),
                    min=min(samples),
                    max=max(samples),
                    std=statistics.pstdev(samples),
                )
        properties = torch.cuda.get_device_properties(rank)
        report = dict(
            rank=rank,
            configuration=vars(args),
            stages=records,
            device=torch.cuda.get_device_name(rank),
            device_uuid=str(getattr(properties, "uuid", "unknown")),
            compute_capability=[properties.major, properties.minor],
            peer_access=[
                peer == rank or torch.cuda.can_device_access_peer(rank, peer)
                for peer in range(args.ep_size)
            ],
            torch_version=torch.__version__,
            cuda_version=torch.version.cuda,
            timing_source="cuda_events_eager",
        )
        (directory / f"rank_{rank}.json").write_text(json.dumps(report))
    finally:
        if comm is not None:
            comm.destroy()
        dist.destroy_process_group()


def run_moe_ep_comm_test(args):
    import torch
    import torch.distributed as dist
    import torch.multiprocessing as mp

    output = Path(args.output_file)
    output.unlink(missing_ok=True)
    if dist.is_initialized():
        raise RuntimeError(
            "moe_ep_comm launches its own local ranks; do not use torchrun/MPI"
        )
    if not torch.cuda.is_available() or torch.cuda.device_count() < args.ep_size:
        raise RuntimeError(
            f"moe_ep_comm needs {args.ep_size} visible NVLink-connected GPUs"
        )
    with tempfile.TemporaryDirectory(prefix="flashinfer_moe_ep_") as directory:
        mp.spawn(_rank_worker, args=(args, directory), nprocs=args.ep_size, join=True)
        reports = [
            json.loads((Path(directory) / f"rank_{rank}.json").read_text())
            for rank in range(args.ep_size)
        ]
    rows = report_rows(reports, args)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(dict(configuration=vars(args), ranks=reports, rows=rows), indent=2)
        + "\n"
    )
    for row in rows:
        print(
            f"[PERF] {args.case_tag} stage={row['schedule_stage']} combine={row['median_time']:.6f} ms dispatch={row['dispatch_median_time']:.6f} ms",
            flush=True,
        )
    return rows
