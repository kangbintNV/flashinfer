"""Host-only CLI and artifact-contract tests; runnable without CUDA or torch."""

import ast
import copy
import importlib.util
import shlex
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[3]
BENCHMARKS = ROOT / "benchmarks"
sys.path.insert(0, str(BENCHMARKS))
moe_ep_comm = importlib.import_module("routines.moe_ep_comm")


CASE = shlex.split(
    "--routine moe_ep_comm --backend nvlink_two_sided --ep_size 2 "
    "--rank_token_schedule 0,128 --hidden_size 4096 --top_k 2 "
    "--num_experts 8 --quant bf16 --expert_output_ndim 3 "
    "--output_mode provided --max_num_tokens_per_rank 128 --warmup 20 "
    "--iters 200 --no_cuda_graph --perfect_router --iter_stats "
    "--output_file raw.json --refcheck --use_cuda_events --case_tag test-empty"
)


def shared_cli():
    tree = ast.parse(
        (BENCHMARKS / "routines/flashinfer_benchmark_utils.py").read_text()
    )
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in (
                "benchmark_apis",
                "output_column_dict",
                "full_output_columns",
            ):
                exec(
                    compile(
                        ast.Module(body=[node], type_ignores=[]), "<registry>", "exec"
                    ),
                    values,
                )
    utilities = types.ModuleType("routines.flashinfer_benchmark_utils")
    utilities.benchmark_apis = values["benchmark_apis"]
    utilities.full_output_columns = values["full_output_columns"]
    spec = importlib.util.spec_from_file_location(
        "tested_benchmark", BENCHMARKS / "flashinfer_benchmark.py"
    )
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, {utilities.__name__: utilities}):
        spec.loader.exec_module(module)
    return module


class TestMoeEpCommBenchmark(unittest.TestCase):
    def setUp(self):
        self.cli = shared_cli()
        self.args = self.cli.parse_args(CASE)

    def reports(self):
        return [
            dict(
                rank=rank,
                configuration=vars(self.args).copy(),
                stages=[
                    dict(
                        counts=[0, 128],
                        preflight=True,
                        postflight=True,
                        valid_received_rows=128,
                        return_collective_calls=1,
                        dispatch_ms=[0.01 + rank * 0.01] * 200,
                        combine_ms=[0.02 + rank * 0.01] * 200,
                    )
                ],
            )
            for rank in range(2)
        ]

    def test_shared_parser_and_aliases(self):
        self.assertEqual((self.args.dry_run_iters, self.args.num_iters), (20, 200))
        self.assertFalse(self.args.use_cupti)
        self.assertIn("moe_ep_comm", self.cli.benchmark_apis["moe_comm"])
        self.assertIn("rank_token_schedule", self.cli.full_output_columns)

    def test_schedule_transitions(self):
        self.assertEqual(
            moe_ep_comm.token_schedule("128,128;0,128;128,128", 2, 128),
            [[128, 128], [0, 128], [128, 128]],
        )

    def test_invalid_schedules(self):
        for schedule in ("0,0", "-1,128", "0,129", "128", "0,128;", "x,128"):
            with self.subTest(schedule=schedule), self.assertRaises(ValueError):
                moe_ep_comm.token_schedule(schedule, 2, 128)

    def test_unsupported_backend_rejected(self):
        case = [
            "nvlink_one_sided" if item == "nvlink_two_sided" else item for item in CASE
        ]
        with self.assertRaises(SystemExit):
            self.cli.parse_args(case)

    def test_invalid_shapes_and_missing_gates(self):
        for option, value in (
            ("--hidden_size", "4097"),
            ("--top_k", "1"),
            ("--num_experts", "6"),
            ("--ep_size", "1"),
            ("--iters", "0"),
        ):
            case = CASE.copy()
            case[case.index(option) + 1] = value
            with self.subTest(option=option), self.assertRaises(SystemExit):
                self.cli.parse_args(case)
        for option in ("--no_cuda_graph", "--refcheck"):
            with self.subTest(option=option), self.assertRaises(SystemExit):
                self.cli.parse_args([item for item in CASE if item != option])

    def test_max_rank_combine_metric(self):
        row = moe_ep_comm.report_rows(self.reports(), self.args)[0]
        self.assertAlmostEqual(row["median_time"], 0.03)
        self.assertAlmostEqual(row["dispatch_median_time"], 0.02)
        self.assertEqual(row["measurement_rank"], 1)
        self.assertEqual(row["case_tag"], self.args.case_tag)
        self.assertTrue(row["refcheck_passed"])

    def test_missing_duplicate_or_wrong_identity(self):
        reports = self.reports()
        for malformed in (reports[:1], [reports[0], reports[0]]):
            with self.assertRaises(ValueError):
                moe_ep_comm.report_rows(malformed, self.args)
        reports[0]["configuration"]["hidden_size"] = 8192
        with self.assertRaises(ValueError):
            moe_ep_comm.report_rows(reports, self.args)

    def test_missing_numeric_samples(self):
        for samples in ([], [0.0] * 200, [float("nan")] * 200, [float("inf")] * 200):
            reports = self.reports()
            reports[0]["stages"][0]["combine_ms"] = samples
            with self.subTest(samples=samples[:1]), self.assertRaises(ValueError):
                moe_ep_comm.report_rows(reports, self.args)

    def test_correctness_and_remote_work_required(self):
        for key, value in (
            ("preflight", False),
            ("postflight", False),
            ("return_collective_calls", 0),
            ("valid_received_rows", 0),
            ("counts", [128, 128]),
        ):
            reports = self.reports()
            reports[0]["stages"][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                moe_ep_comm.report_rows(reports, self.args)

    def test_each_schedule_stage_emits_row(self):
        args = copy.copy(self.args)
        args.rank_token_schedule = "128,128;0,128;128,128"
        reports = self.reports()
        for report in reports:
            report["configuration"] = vars(args).copy()
            template = report["stages"][0]
            report["stages"] = [
                dict(copy.deepcopy(template), counts=counts)
                for counts in moe_ep_comm.token_schedule(
                    args.rank_token_schedule, 2, 128
                )
            ]
        self.assertEqual(
            [row["schedule_stage"] for row in moe_ep_comm.report_rows(reports, args)],
            [0, 1, 2],
        )

    def test_shared_dispatch(self):
        with patch.object(moe_ep_comm, "run_moe_ep_comm_test", return_value=[]) as run:
            self.cli.run_test(self.args)
        run.assert_called_once_with(self.args)


if __name__ == "__main__":
    unittest.main()
