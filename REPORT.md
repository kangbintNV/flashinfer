# Bot Run Request Check: one minimal retry demo

Fresh replay of the same 50 merged upstream PRs on existing fork demo PRs #126–#175. No GPU tests were launched. Historical source was read as pinned Git objects, never executed.

## Policy

An authentic historical internal bot reply passes the formal gate immediately. Markdown/RST-only changes skip inference. Otherwise analyze with compact JSON and default thinking. On analysis error or unknown classification, retry once with reasoning_effort=minimal. A reliable CPU-only result passes; GPU changes or unresolved analysis require /bot run and an internal bot reply. A command alone does not pass. No pipeline creation or test-pass requirement is added.

The no-reply diagnostic withholds historical replies to exercise the analysis; its model calls are not evidence that the original explicit /bot run command used an LLM. Formal reply shortcuts do not call the model. The combined experiment computes diagnostics for all non-documentation samples.

## Results

| Metric | Default first attempt | After one minimal retry |
|---|---:|---:|
| Formal passes / 50 | 36 | 36 |
| No-reply passes / 50 | 11 | 11 |
| Unresolved GPU/CPU analysis | 9 | 7 |

Retry triggered for **9** PRs, recovered a validated classification for **2**, and remained unresolved for **7**. Unresolved cases fail with a /bot run instruction; none receives an automatic CPU exemption.

Final classifications: `{"cpu_only": 7, "docs_only": 4, "gpu_required": 32, "unknown": 7}`. Formal reasons: `{"bot_response_found": 30, "bot_run_required_after_retry": 3, "command_missing": 11, "cpu_only": 3, "docs_only": 3}`.

The previous inventory-fix demo had 36/50 formal passes. This rerun also changes JSON presentation and generates fresh model responses, so cross-run changes cannot be attributed only to retry. The within-run default/retry comparison above isolates the added retry step.

## Retry examples

- Upstream #9815 / demo #147: default evidence response was fenced JSON and failed strict parsing. Minimal retried evidence and final selection successfully; GPU-related weight-scale handling was correctly retained as requiring a bot reply even though only a CPU test was selected.
- Upstream #9865 / demo #160: default target selection failed the inspected executable test guard. Minimal returned needs_maintainer with a valid GPU-required classification. This recovers GPU analysis, not an automatically runnable test selection.
- Upstream #9846 / demo #163: default analysis succeeded this round (final selection completion_tokens=1910); no minimal retry was needed. This does not erase the earlier 4000-token truncation observation or guarantee future success.

Remaining failures: {"AI target has no inspected executable test candidate in the merged tree": 1, "Cannot establish a CPU-only exemption: changed-file patches are incomplete.": 3, "GPU-impact evidence was not inspected": 2, "Inference Hub returned invalid JSON": 1}

No formal pass was added by retry in this run: both recovered analyses were GPU-related. Formal blocking reasons became more specific; requests without a qualifying bot reply continue to fail.

## Execution and publication limits

- Same frozen PR metadata, changed files, comments, trusted CI and pinned merged trees: audited 50/50.
- The full-tree inventory guard and all original target/GPU validators remain active. No JSON fence repair, response salvage, inferred-file allowance or CPU exemption on failure.
- Same model azure/anthropic/claude-opus-5, max_tokens=4000 per request, compact output instructions on final analysis only. No thinking disable or budget override.
- Default evidence selection is fresh. If it reaches final selection, that validated file-request response is reused for the minimal retry, preserving the exact final context hash. If file selection itself fails validation, it is retried with minimal instead.
- Analysis is retried at most once. Existing-style transport retries for transient API/network errors are separately recorded and do not discard completed semantic failures.
- This pilot measures validated analysis and merge-gate behavior, not ground-truth accuracy of all 50 classifications. All seven CPU-only predictions were inspected; #9843 is a host-validation test boundary involving a compile-target-specific skip, documented in cpu-exemption-review.json, rather than proof the whole test module runs without a GPU.
- All saved model results were independently replayed through the original validators for all 50 PRs, including identical context hashes and the original failure outcomes; see offline-verification.json.
- Current personal GitHub credentials cannot create Check Runs (HTTP 403: GitHub App required). Results are published as commit statuses visible in the PR checks area, linked to this immutable report. Existing Check Runs, fork main, product PR and workflows are untouched.
- Detailed raw model responses, including reasoning fields, remain local and are not published. No secrets or PR comments are posted.

## All 50 PRs

| Upstream | Demo | Formal result | Final classification | Retry |
|---|---|---|---|---|
| [#10013](https://github.com/flashinfer-ai/flashinfer/pull/10013) | [#127](https://github.com/kangbintNV/flashinfer/pull/127) | bot_response_found | gpu_required | no |
| [#9788](https://github.com/flashinfer-ai/flashinfer/pull/9788) | [#126](https://github.com/kangbintNV/flashinfer/pull/126) | cpu_only | cpu_only | no |
| [#10006](https://github.com/flashinfer-ai/flashinfer/pull/10006) | [#130](https://github.com/kangbintNV/flashinfer/pull/130) | command_missing | gpu_required | no |
| [#10005](https://github.com/flashinfer-ai/flashinfer/pull/10005) | [#129](https://github.com/kangbintNV/flashinfer/pull/129) | command_missing | gpu_required | no |
| [#9989](https://github.com/flashinfer-ai/flashinfer/pull/9989) | [#131](https://github.com/kangbintNV/flashinfer/pull/131) | bot_response_found | gpu_required | no |
| [#9731](https://github.com/flashinfer-ai/flashinfer/pull/9731) | [#128](https://github.com/kangbintNV/flashinfer/pull/128) | bot_response_found | gpu_required | no |
| [#9916](https://github.com/flashinfer-ai/flashinfer/pull/9916) | [#133](https://github.com/kangbintNV/flashinfer/pull/133) | bot_response_found | gpu_required | no |
| [#9990](https://github.com/flashinfer-ai/flashinfer/pull/9990) | [#132](https://github.com/kangbintNV/flashinfer/pull/132) | bot_response_found | cpu_only | no |
| [#9978](https://github.com/flashinfer-ai/flashinfer/pull/9978) | [#134](https://github.com/kangbintNV/flashinfer/pull/134) | bot_response_found | gpu_required | no |
| [#9964](https://github.com/flashinfer-ai/flashinfer/pull/9964) | [#135](https://github.com/kangbintNV/flashinfer/pull/135) | bot_response_found | gpu_required | no |
| [#9958](https://github.com/flashinfer-ai/flashinfer/pull/9958) | [#136](https://github.com/kangbintNV/flashinfer/pull/136) | bot_response_found | gpu_required | no |
| [#9991](https://github.com/flashinfer-ai/flashinfer/pull/9991) | [#137](https://github.com/kangbintNV/flashinfer/pull/137) | bot_response_found | unknown | yes |
| [#9817](https://github.com/flashinfer-ai/flashinfer/pull/9817) | [#138](https://github.com/kangbintNV/flashinfer/pull/138) | bot_run_required_after_retry | unknown | yes |
| [#9716](https://github.com/flashinfer-ai/flashinfer/pull/9716) | [#139](https://github.com/kangbintNV/flashinfer/pull/139) | bot_response_found | gpu_required | no |
| [#9974](https://github.com/flashinfer-ai/flashinfer/pull/9974) | [#140](https://github.com/kangbintNV/flashinfer/pull/140) | command_missing | gpu_required | no |
| [#9892](https://github.com/flashinfer-ai/flashinfer/pull/9892) | [#141](https://github.com/kangbintNV/flashinfer/pull/141) | bot_response_found | gpu_required | no |
| [#9885](https://github.com/flashinfer-ai/flashinfer/pull/9885) | [#142](https://github.com/kangbintNV/flashinfer/pull/142) | bot_response_found | gpu_required | no |
| [#9651](https://github.com/flashinfer-ai/flashinfer/pull/9651) | [#143](https://github.com/kangbintNV/flashinfer/pull/143) | bot_response_found | gpu_required | no |
| [#9876](https://github.com/flashinfer-ai/flashinfer/pull/9876) | [#144](https://github.com/kangbintNV/flashinfer/pull/144) | command_missing | gpu_required | no |
| [#9917](https://github.com/flashinfer-ai/flashinfer/pull/9917) | [#145](https://github.com/kangbintNV/flashinfer/pull/145) | bot_response_found | gpu_required | no |
| [#9816](https://github.com/flashinfer-ai/flashinfer/pull/9816) | [#146](https://github.com/kangbintNV/flashinfer/pull/146) | command_missing | gpu_required | no |
| [#9815](https://github.com/flashinfer-ai/flashinfer/pull/9815) | [#147](https://github.com/kangbintNV/flashinfer/pull/147) | command_missing | gpu_required | yes |
| [#9814](https://github.com/flashinfer-ai/flashinfer/pull/9814) | [#148](https://github.com/kangbintNV/flashinfer/pull/148) | cpu_only | cpu_only | no |
| [#9813](https://github.com/flashinfer-ai/flashinfer/pull/9813) | [#149](https://github.com/kangbintNV/flashinfer/pull/149) | bot_response_found | gpu_required | no |
| [#9771](https://github.com/flashinfer-ai/flashinfer/pull/9771) | [#150](https://github.com/kangbintNV/flashinfer/pull/150) | bot_response_found | gpu_required | no |
| [#9819](https://github.com/flashinfer-ai/flashinfer/pull/9819) | [#151](https://github.com/kangbintNV/flashinfer/pull/151) | command_missing | gpu_required | no |
| [#9908](https://github.com/flashinfer-ai/flashinfer/pull/9908) | [#152](https://github.com/kangbintNV/flashinfer/pull/152) | cpu_only | cpu_only | no |
| [#9897](https://github.com/flashinfer-ai/flashinfer/pull/9897) | [#153](https://github.com/kangbintNV/flashinfer/pull/153) | bot_response_found | gpu_required | no |
| [#9844](https://github.com/flashinfer-ai/flashinfer/pull/9844) | [#154](https://github.com/kangbintNV/flashinfer/pull/154) | bot_response_found | gpu_required | no |
| [#9843](https://github.com/flashinfer-ai/flashinfer/pull/9843) | [#155](https://github.com/kangbintNV/flashinfer/pull/155) | bot_response_found | cpu_only | no |
| [#9694](https://github.com/flashinfer-ai/flashinfer/pull/9694) | [#156](https://github.com/kangbintNV/flashinfer/pull/156) | bot_response_found | unknown | yes |
| [#9847](https://github.com/flashinfer-ai/flashinfer/pull/9847) | [#157](https://github.com/kangbintNV/flashinfer/pull/157) | bot_response_found | cpu_only | no |
| [#9861](https://github.com/flashinfer-ai/flashinfer/pull/9861) | [#158](https://github.com/kangbintNV/flashinfer/pull/158) | bot_response_found | gpu_required | no |
| [#9871](https://github.com/flashinfer-ai/flashinfer/pull/9871) | [#159](https://github.com/kangbintNV/flashinfer/pull/159) | bot_response_found | gpu_required | no |
| [#9865](https://github.com/flashinfer-ai/flashinfer/pull/9865) | [#160](https://github.com/kangbintNV/flashinfer/pull/160) | bot_response_found | gpu_required | yes |
| [#9894](https://github.com/flashinfer-ai/flashinfer/pull/9894) | [#161](https://github.com/kangbintNV/flashinfer/pull/161) | bot_response_found | cpu_only | no |
| [#9836](https://github.com/flashinfer-ai/flashinfer/pull/9836) | [#162](https://github.com/kangbintNV/flashinfer/pull/162) | bot_response_found | gpu_required | no |
| [#9846](https://github.com/flashinfer-ai/flashinfer/pull/9846) | [#163](https://github.com/kangbintNV/flashinfer/pull/163) | command_missing | gpu_required | no |
| [#9749](https://github.com/flashinfer-ai/flashinfer/pull/9749) | [#164](https://github.com/kangbintNV/flashinfer/pull/164) | bot_response_found | gpu_required | no |
| [#9858](https://github.com/flashinfer-ai/flashinfer/pull/9858) | [#165](https://github.com/kangbintNV/flashinfer/pull/165) | command_missing | gpu_required | no |
| [#9857](https://github.com/flashinfer-ai/flashinfer/pull/9857) | [#166](https://github.com/kangbintNV/flashinfer/pull/166) | command_missing | gpu_required | no |
| [#9834](https://github.com/flashinfer-ai/flashinfer/pull/9834) | [#167](https://github.com/kangbintNV/flashinfer/pull/167) | command_missing | gpu_required | no |
| [#9818](https://github.com/flashinfer-ai/flashinfer/pull/9818) | [#168](https://github.com/kangbintNV/flashinfer/pull/168) | bot_run_required_after_retry | unknown | yes |
| [#9358](https://github.com/flashinfer-ai/flashinfer/pull/9358) | [#169](https://github.com/kangbintNV/flashinfer/pull/169) | docs_only | docs_only | no |
| [#9332](https://github.com/flashinfer-ai/flashinfer/pull/9332) | [#170](https://github.com/kangbintNV/flashinfer/pull/170) | bot_run_required_after_retry | unknown | yes |
| [#9307](https://github.com/flashinfer-ai/flashinfer/pull/9307) | [#171](https://github.com/kangbintNV/flashinfer/pull/171) | bot_response_found | unknown | yes |
| [#9545](https://github.com/flashinfer-ai/flashinfer/pull/9545) | [#172](https://github.com/kangbintNV/flashinfer/pull/172) | bot_response_found | docs_only | no |
| [#8464](https://github.com/flashinfer-ai/flashinfer/pull/8464) | [#173](https://github.com/kangbintNV/flashinfer/pull/173) | bot_response_found | unknown | yes |
| [#8960](https://github.com/flashinfer-ai/flashinfer/pull/8960) | [#174](https://github.com/kangbintNV/flashinfer/pull/174) | docs_only | docs_only | no |
| [#8930](https://github.com/flashinfer-ai/flashinfer/pull/8930) | [#175](https://github.com/kangbintNV/flashinfer/pull/175) | docs_only | docs_only | no |

## Per-PR details

### PR 10013

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/10013) · [Demo #127](https://github.com/kangbintNV/flashinfer/pull/127)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/10013#issuecomment-7152368777)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated gpu_required

Final: `gpu_required`. Head-major inputs are transposed/copied on device then fed to the fused NCCL symmetric-memory A2A+LSE kernel; new numerical equivalence test compares against distributed reference

Selected tests: `tests/comm/test_dcp_lse_reduce.py`

### PR 9788

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9788) · [Demo #126](https://github.com/kangbintNV/flashinfer/pull/126)

Formal: **success / cpu_only**. No-reply diagnostic: **cpu_only**.

Single packaging version string consumed by pyproject dynamic version and flashinfer/version.py; no kernel, launcher, dtype/layout, JIT/AOT build logic changed, so GPU-free validation suffices.

Evidence: version.txt, pyproject.toml, flashinfer/version.py

Test selection gap: Runtime version-matching of flashinfer-cubin/jit-cache wheels (artifacts.py not inspected) is unverified for the new version.

- default: validated cpu_only

Final: `cpu_only`. Single packaging version string consumed by pyproject dynamic version and flashinfer/version.py; no kernel, launcher, dtype/layout, JIT/AOT build logic changed, so GPU-free validation suffices.

### PR 10006

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/10006) · [Demo #130](https://github.com/kangbintNV/flashinfer/pull/130)

Formal: **failure / command_missing**. No-reply diagnostic: **command_missing**.

Script selects the nvidia-nccl-cuXX wheel/libnccl runtime used by NCCL-EP collectives and re-asserts the pin after install; wrong version breaks torch import and multi-GPU EP communication, needing the cu134 EP lane.

Evidence: docker/install/build_flashinfer_ep_pytorch.sh, tests/infra/test_sharding/test_shell_entrypoint.py

Test selection gap: No pytest covers the real installer's NCCL selection; validation relies on the multi-GPU EP container lane.

GPU-related changes: comment `/bot run` and wait for `flashinfer-bot` to reply.

- default: validated gpu_required

Final: `gpu_required`. Script selects the nvidia-nccl-cuXX wheel/libnccl runtime used by NCCL-EP collectives and re-asserts the pin after install; wrong version breaks torch import and multi-GPU EP communication, needing the cu134 EP lane.

### PR 10005

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/10005) · [Demo #129](https://github.com/kangbintNV/flashinfer/pull/129)

Formal: **failure / command_missing**. No-reply diagnostic: **command_missing**.

Constrains cuda-core&amp;lt;1.3 in the CI image, changing the CUDA bindings/memory-resource stack nvshmem4py uses; NVSHMEM collection and GPU comm runs need GPU validation beyond import checks.

Evidence: docker/install/install_python_packages.sh, tests/cpu/infra/test_cuda_tile_ci.py

Suggested tests: tests/cpu/infra/test_cuda_tile_ci.py

Test selection gap: No selected test exercises nvshmem4py import/allocation on GPU (e.g. tests/comm NVSHMEM cases); image must be rebuilt and pins updated first.

GPU-related changes: comment `/bot run` and wait for `flashinfer-bot` to reply.

- default: validated gpu_required

Final: `gpu_required`. Constrains cuda-core&lt;1.3 in the CI image, changing the CUDA bindings/memory-resource stack nvshmem4py uses; NVSHMEM collection and GPU comm runs need GPU validation beyond import checks.

Selected tests: `tests/cpu/infra/test_cuda_tile_ci.py`

### PR 9989

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9989) · [Demo #131](https://github.com/kangbintNV/flashinfer/pull/131)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9989#issuecomment-7141676310)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated gpu_required

Final: `gpu_required`. New sm_90a CUDA kernels/bindings, changed launch planning (one launch per call), split item-table upload and CUDA-graph capture semantics; correctness/numerics need Hopper execution, not CPU checks.

Selected tests: `tests/gdp`

### PR 9731

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9731) · [Demo #128](https://github.com/kangbintNV/flashinfer/pull/128)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9731#issuecomment-7117140767)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated gpu_required

Final: `gpu_required`. Split-K grid sizing, kernel compile flag schedule_whole_tiles, per-plan lock buffers and cross-CTA reduction order change GEMM launch and numerics; only GPU execution validates.

Selected tests: `tests/experimental/b12x/gemm/test_trellis_linear.py`

### PR 9916

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9916) · [Demo #133](https://github.com/kangbintNV/flashinfer/pull/133)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9916#issuecomment-7119623448)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated gpu_required

Final: `gpu_required`. Adds a Triton CUDA kernel staging MXFP8 activations/scale swizzle into workspace buffers and changes dispatch gating in stage_shared_inputs; byte-exact and CUDA-graph behavior needs GPU.

Selected tests: `tests/moe_ep/test_sm107_shared_staging.py`, `tests/moe_ep/test_sm107_shared_expert.py`

### PR 9990

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9990) · [Demo #132](https://github.com/kangbintNV/flashinfer/pull/132)

Formal: **success / bot_response_found**. No-reply diagnostic: **cpu_only**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9990#issuecomment-7137423935)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated cpu_only

Final: `cpu_only`. Only interpreter floor and docs changed; no kernels, bindings, JIT/AOT or dispatch logic altered, so GPU-free validation (build metadata/TOML checks, lint) suffices.

### PR 9978

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9978) · [Demo #134](https://github.com/kangbintNV/flashinfer/pull/134)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9978#issuecomment-7130412330)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated gpu_required

Final: `gpu_required`. New test runs cold NVFP4 MoE GEMM2 autotuning and asserts CUDA profiler records a fused FINALIZE kernel; validating kernel selection/profiling needs a Blackwell GPU, not CPU.

### PR 9964

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9964) · [Demo #135](https://github.com/kangbintNV/flashinfer/pull/135)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9964#issuecomment-7131410753)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated gpu_required

Final: `gpu_required`. Changed tests launch CUDA kernels: BF16 warp split-K GEMM with PDL bias ordering via an NVRTC late_store producer, and SM100/SM103 cluster top-k with delayed seq_lens; CPU validation cannot check these.

### PR 9958

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9958) · [Demo #136](https://github.com/kangbintNV/flashinfer/pull/136)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9958#issuecomment-7122388075)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated gpu_required

Final: `gpu_required`. Added parameterized case runs BatchPrefillTSWrapper on device='cuda' with 16K Q/KV, BF16/E4M3 Q/K and E4M3 V, checking kernel rescaling after a later KV tile raises row max; CPU validation insufficient.

### PR 9991

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9991) · [Demo #137](https://github.com/kangbintNV/flashinfer/pull/137)

Formal: **success / bot_response_found**. No-reply diagnostic: **bot_run_required_after_retry**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9991#issuecomment-7137430127)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: GPU-impact evidence was not inspected
- minimal: GPU-impact evidence was not inspected

Final: `unknown`. GPU-impact evidence was not inspected

### PR 9817

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9817) · [Demo #138](https://github.com/kangbintNV/flashinfer/pull/138)

Formal: **failure / bot_run_required_after_retry**. No-reply diagnostic: **bot_run_required_after_retry**.

Unable to reliably establish a CPU-only exemption after the default analysis and one minimal retry.

- default: GPU-impact evidence was not inspected
- minimal: GPU-impact evidence was not inspected

Comment `/bot run` or `/bot run tests/...` and wait for the internal bot response.

- default: GPU-impact evidence was not inspected
- minimal: GPU-impact evidence was not inspected

Final: `unknown`. GPU-impact evidence was not inspected

### PR 9716

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9716) · [Demo #139](https://github.com/kangbintNV/flashinfer/pull/139)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9716#issuecomment-7119967898)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated gpu_required

Final: `gpu_required`. Binding dtype checks now float8_e4m3fn, wrapper drops uint8 views and launches entry directly, and kernel adds sm_103a griddepcontrol.launch_dependents (PDL); needs GPU launch validation.

Selected tests: `tests/attention/test_cake_sage_block_sparse_attention_sm100_api.py`

### PR 9974

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9974) · [Demo #140](https://github.com/kangbintNV/flashinfer/pull/140)

Formal: **failure / command_missing**. No-reply diagnostic: **command_missing**.

Device item-table allocation, pinned-host copies and CUDA graph capture/replay semantics changed; correctness only observable via capture-then-eager GPU execution.

Evidence: flashinfer/cake_gdp_backend/__init__.py, tests/gdp/test_cake_gdp_prefill_bw.py

Suggested tests: tests/gdp

Test selection gap: Blackwell-only regression test skips on A10G/T4/H100 lanes; no routed lane validates the capture-first path.

GPU-related changes: comment `/bot run` and wait for `flashinfer-bot` to reply.

- default: validated gpu_required

Final: `gpu_required`. Device item-table allocation, pinned-host copies and CUDA graph capture/replay semantics changed; correctness only observable via capture-then-eager GPU execution.

Selected tests: `tests/gdp`

### PR 9892

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9892) · [Demo #141](https://github.com/kangbintNV/flashinfer/pull/141)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9892#issuecomment-7131921554)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated gpu_required

Final: `gpu_required`. Changes MXFP8 CuTe-DSL runner tactic-pool cache identity, affecting autotuned kernel selection and winners served on SM100/SM103/SM107 GEMM paths; real kernel/cache behavior needs GPU validation.

Selected tests: `tests/cpu/gemm/test_mxfp8_precompile.py`

### PR 9885

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9885) · [Demo #142](https://github.com/kangbintNV/flashinfer/pull/142)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9885#issuecomment-7122274355)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated gpu_required

Final: `gpu_required`. Changes sm_107a batch DeepGEMM FP8 dispatch: homed weights route to the masked pair kernel program from expected_m 128; PR also adds a device kernel test timing per-SM remote vs local memory loads.

### PR 9651

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9651) · [Demo #143](https://github.com/kangbintNV/flashinfer/pull/143)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9651#issuecomment-7120452466)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated gpu_required

Final: `gpu_required`. Rewrites warp-collective block-scaled MMA inline PTX, scale byte selectors and side-effect annotation in SM120 CuTeDSL kernels; only GPU execution validates numerics/codegen.

Selected tests: `tests/moe_ep/test_moe_ep_sm120_w4a8_cutedsl_mega.py`

### PR 9876

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9876) · [Demo #144](https://github.com/kangbintNV/flashinfer/pull/144)

Formal: **failure / command_missing**. No-reply diagnostic: **command_missing**.

Changes add TMA gather4 NVFP4 scale copies, a route-order CLC work-queue mapping, metadata-kernel counting sort with new FFI tensors, and plan-time balanced_scheduler/compile-spec selection; correctness needs real kernel execution.

Evidence: csrc/prims_ts_q_token_kv_block_sparse_metadata_jit_binding.cu, flashinfer/attention/prims_ts/kernels/fmha_decode/fmha_decode_resources/smem_resources.py, flashinfer/attention/prims_ts/kernels/fmha_decode/fmha_decode_tasks.py

Test selection gap: No inspected test body confirms coverage of gather4 scale staging, route-order dispatch, or the new plan(balanced_scheduler=...) option.

GPU-related changes: comment `/bot run` and wait for `flashinfer-bot` to reply.

- default: validated gpu_required

Final: `gpu_required`. Changes add TMA gather4 NVFP4 scale copies, a route-order CLC work-queue mapping, metadata-kernel counting sort with new FFI tensors, and plan-time balanced_scheduler/compile-spec selection; correctness needs real kernel execution.

### PR 9917

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9917) · [Demo #145](https://github.com/kangbintNV/flashinfer/pull/145)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9917#issuecomment-7118627807)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated gpu_required

Final: `gpu_required`. Adds sm_100a/sm_103a CUDA kernels, bindings, AOT build.json entries and Blackwell launch planning/dispatch with pinned item table and CUDA-graph capture; needs device validation.

Selected tests: `tests/gdp/test_cake_gdp_prefill_bw.py`, `tests/gdp/test_cake_gdp_prefill_api.py`, `tests/gdp/test_cake_gdp_prefill_route.py`, `tests/cpu/gdp/test_cake_gdp_prefill_bw_plan.py`

### PR 9816

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9816) · [Demo #146](https://github.com/kangbintNV/flashinfer/pull/146)

Formal: **failure / command_missing**. No-reply diagnostic: **command_missing**.

Validation now constrains Hopper blockwise FP8 MMA tile K to 128, changing accepted launch geometry/FC2 scale indexing for the SM90 pull FP8 megakernel and mxfp4 proxy config; correctness needs GPU runs.

Evidence: flashinfer/moe_ep/shims/sm90/cutedsl_megamoe/tuner.py, flashinfer/moe_ep/shims/sm90/cutedsl_megamoe/hopper_mxfp4.py, tests/moe_ep/test_sm90_pull_fp8_tuner.py

Suggested tests: tests/moe_ep/test_sm90_pull_fp8_tuner.py

Test selection gap: No inspected GPU kernel-vs-reference case covering blockwise FP8 K=128 enforcement or the mxfp4 proxy tile-K rewrite.

GPU-related changes: comment `/bot run` and wait for `flashinfer-bot` to reply.

- default: validated gpu_required

Final: `gpu_required`. Validation now constrains Hopper blockwise FP8 MMA tile K to 128, changing accepted launch geometry/FC2 scale indexing for the SM90 pull FP8 megakernel and mxfp4 proxy config; correctness needs GPU runs.

Selected tests: `tests/moe_ep/test_sm90_pull_fp8_tuner.py`

### PR 9815

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9815) · [Demo #147](https://github.com/kangbintNV/flashinfer/pull/147)

Formal: **failure / command_missing**. No-reply diagnostic: **command_missing**.

Changes how SM100 NVFP4 kernel-ready weight scales are reinterpreted (uint8 bytes viewed as float8_e4m3fn) before kernel/validator consumption; dtype/layout correctness needs GPU execution.

Evidence: flashinfer/moe_ep/backends/mega/kernel/sm100/standard_cutedsl.py, flashinfer/moe_ep/core/kernel/base.py, tests/cpu/moe_ep/test_megamoe_refresh_contracts.py

Suggested tests: tests/cpu/moe_ep/test_megamoe_refresh_contracts.py

Test selection gap: No inspected GPU test exercises SM100 NVFP4 mega kernel execution with byte-view scales end to end.

GPU-related changes: comment `/bot run` and wait for `flashinfer-bot` to reply.

- default: Inference Hub returned invalid JSON
- minimal: validated gpu_required

Final: `gpu_required`. Changes how SM100 NVFP4 kernel-ready weight scales are reinterpreted (uint8 bytes viewed as float8_e4m3fn) before kernel/validator consumption; dtype/layout correctness needs GPU execution.

Selected tests: `tests/cpu/moe_ep/test_megamoe_refresh_contracts.py`

### PR 9814

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9814) · [Demo #148](https://github.com/kangbintNV/flashinfer/pull/148)

Formal: **success / cpu_only**. No-reply diagnostic: **cpu_only**.

Changed lines only pick a CTAs-per-token constant for the reported baseline_grid_ctas metadata; kernel launches, runners, shapes and validation paths are unchanged, so GPU-free review suffices.

Evidence: benchmarks/bench_cake_megamoe_topk_reduce.py, .github/workflows/pr-test.yml

- default: validated cpu_only

Final: `cpu_only`. Changed lines only pick a CTAs-per-token constant for the reported baseline_grid_ctas metadata; kernel launches, runners, shapes and validation paths are unchanged, so GPU-free review suffices.

### PR 9813

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9813) · [Demo #149](https://github.com/kangbintNV/flashinfer/pull/149)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9813#issuecomment-7073352142)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated gpu_required

Final: `gpu_required`. Changed fixtures gate MegaMoE knob-cache lookup, which selects compiled kernel tile/cluster knobs and symm workspace config; validation needs Blackwell GPUs

Selected tests: `tests/moe_ep/test_workspace_pool.py`, `tests/moe_ep/test_bf16_mxfp8_cutedsl_kernel_vs_reference.py`

### PR 9771

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9771) · [Demo #150](https://github.com/kangbintNV/flashinfer/pull/150)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9771#issuecomment-7093273577)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated gpu_required

Final: `gpu_required`. Changes tcgen05 MMA issue, TMEM/SMEM ring layout, NVFP4 dense-multiply converters, split-reducer barriers and D512 profile auto-selection; only device execution validates numerics.

Selected tests: `tests/attention/test_attention_ts_decode_mixed_precision.py`

### PR 9819

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9819) · [Demo #151](https://github.com/kangbintNV/flashinfer/pull/151)

Formal: **failure / command_missing**. No-reply diagnostic: **command_missing**.

Change adds positive-count validation for sf_pusher_cta_count in the Blackwell GenPhase kernel, which governs scale-factor publisher CTA geometry; valid launches still need SM100/103 kernel execution validation.

Evidence: flashinfer/moe_ep/kernels/cutedsl_megamoe/sources/kernel_src/blackwell/inference/genphase/token_comm_gen_specialized.py, tests/moe_ep/test_sm100_genphase_dtypes.py

Suggested tests: tests/moe_ep/test_sm100_genphase_dtypes.py, tests/cpu/moe_ep/test_provider_package_isolation.py

Test selection gap: Only the rejection path is newly covered; positive-count GenPhase graph cases rely on existing arch_blackwell tests that current PR lanes may not schedule.

GPU-related changes: comment `/bot run` and wait for `flashinfer-bot` to reply.

- default: validated gpu_required

Final: `gpu_required`. Change adds positive-count validation for sf_pusher_cta_count in the Blackwell GenPhase kernel, which governs scale-factor publisher CTA geometry; valid launches still need SM100/103 kernel execution validation.

Selected tests: `tests/moe_ep/test_sm100_genphase_dtypes.py`, `tests/cpu/moe_ep/test_provider_package_isolation.py`

### PR 9908

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9908) · [Demo #152](https://github.com/kangbintNV/flashinfer/pull/152)

Formal: **success / cpu_only**. No-reply diagnostic: **cpu_only**.

Change only disables H100 matrix entries in GitHub Actions workflow logic; no kernel, binding, dispatch or runtime behavior altered, so GPU-free validation of YAML/shell gating suffices.

Evidence: .github/workflows/pr-test.yml

Test selection gap: No inspected test asserts RUN_H100 gating; H100 lane coverage is suspended until the flag is restored.

- default: validated cpu_only

Final: `cpu_only`. Change only disables H100 matrix entries in GitHub Actions workflow logic; no kernel, binding, dispatch or runtime behavior altered, so GPU-free validation of YAML/shell gating suffices.

### PR 9897

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9897) · [Demo #153](https://github.com/kangbintNV/flashinfer/pull/153)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9897#issuecomment-7115181575)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated gpu_required

Final: `gpu_required`. Moved cases execute FP8/NVFP4 mixed-precision PrimTS paged decode kernels on Blackwell; numerical validation needs GPU, CPU-only collection proves nothing.

Selected tests: `tests/attention/test_attention_ts_decode_mixed_precision.py`

### PR 9844

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9844) · [Demo #154](https://github.com/kangbintNV/flashinfer/pull/154)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9844#issuecomment-7076553375)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated gpu_required

Final: `gpu_required`. Change guards a CUDA-graph replay/profiler fill-count assertion in a MoE batch-invariant test; the exercised path needs CUDA graph capture, kernel launches and CUPTI, so GPU-free validation is insufficient.

### PR 9843

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9843) · [Demo #155](https://github.com/kangbintNV/flashinfer/pull/155)

Formal: **success / bot_response_found**. No-reply diagnostic: **cpu_only**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9843#issuecomment-7076551897)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated cpu_only

Final: `cpu_only`. Test-only edit: derives KV256 ring depth from static SMEM constants and host-side config/schedule validation plus a compile-target arch query; no kernel launch or library change.

### PR 9694

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9694) · [Demo #156](https://github.com/kangbintNV/flashinfer/pull/156)

Formal: **success / bot_response_found**. No-reply diagnostic: **bot_run_required_after_retry**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9694#issuecomment-7035450417)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: AI target has no inspected executable test candidate in the merged tree
- minimal: AI target has no inspected executable test candidate in the merged tree

Final: `unknown`. AI target has no inspected executable test candidate in the merged tree

### PR 9847

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9847) · [Demo #157](https://github.com/kangbintNV/flashinfer/pull/157)

Formal: **success / bot_response_found**. No-reply diagnostic: **cpu_only**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9847#issuecomment-7077462090)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated cpu_only

Final: `cpu_only`. Test-only change to locating provider manifest and vendored sources; assertions are JSON manifest and SHA-256 file checks plus a subprocess with no CUDA use, so GPU-free validation suffices

Selected tests: `tests/cpu/moe_ep/test_provider_package_isolation.py`, `tests/moe_ep/test_provider_package.py`

### PR 9861

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9861) · [Demo #158](https://github.com/kangbintNV/flashinfer/pull/158)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9861#issuecomment-7094014552)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated gpu_required

Final: `gpu_required`. Tests spawn NCCL ranks, allocate IPC workspaces, capture CUDA graphs and compare FP4-swizzled scale-factor buffer writes against kernel output; no CPU-only validation possible

Selected tests: `tests/comm/test_trtllm_moe_allreduce_fusion_finalize.py`, `tests/comm/test_trtllm_moe_allreduce_fusion.py`

### PR 9871

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9871) · [Demo #159](https://github.com/kangbintNV/flashinfer/pull/159)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9871#issuecomment-7102324850)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated gpu_required

Final: `gpu_required`. Changed tests exercise CUDA FP4/MXFP8 GEMM kernels, b12x tactic enumeration, autotune buckets, CUDA graph replay and output-buffer guards; no CPU-only validation possible.

Selected tests: `tests/gemm/test_mm_fp4.py`

### PR 9865

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9865) · [Demo #160](https://github.com/kangbintNV/flashinfer/pull/160)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9865#issuecomment-7093929737)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: AI target has no inspected executable test candidate in the merged tree
- minimal: validated gpu_required

Final: `gpu_required`. Patch strengthens a persistent prims-ts decode sink test with exact inactive-row checks and a captured CUDA graph replayed across KV-length states; validating kernel writes and graph replay needs a GPU.

### PR 9894

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9894) · [Demo #161](https://github.com/kangbintNV/flashinfer/pull/161)

Formal: **success / bot_response_found**. No-reply diagnostic: **cpu_only**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9894#issuecomment-7106000551)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated cpu_only

Final: `cpu_only`. Change is confined to test doubles: fake capture accepts pool and torch.cuda.current_device/graph_pool_handle are patched, so the profiler path runs on Gloo subprocesses with no real CUDA call.

Selected tests: `tests/autotuner/test_cupti_distributed.py`

### PR 9836

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9836) · [Demo #162](https://github.com/kangbintNV/flashinfer/pull/162)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9836#issuecomment-7091022464)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated gpu_required

Final: `gpu_required`. Changes affect DLPack strides for staging kernels, NVFP4 JIT min_cuda (E2M1 ptxas miscompile), cooperative-launch refusal under CUDA graph capture, and NCCL barrier/device binding; all need GPU validation.

Selected tests: `tests/experimental/test_cake_nvfp4_attention_api.py`, `tests/moe_ep/test_bf16_stage.py`, `tests/comm/test_cake_dcp_alltoall.py`

### PR 9846

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9846) · [Demo #163](https://github.com/kangbintNV/flashinfer/pull/163)

Formal: **failure / command_missing**. No-reply diagnostic: **command_missing**.

Changes softmax mask-tile selection in FMHA context/decode and MLA decode kernels (task cache words, SMEM packed range, FP8 swaps score masking); numerics need GPU execution.

Evidence: flashinfer/attention/prims_ts/kernels/fmha_decode/fmha_decode_resources/tmem_s.py, flashinfer/attention/prims_ts/kernels/mla_decode/throughput_latency_1cta/resources/tmem_s.py, tests/attention/test_attention_ts_mla_cp.py

Suggested tests: tests/attention/test_attention_ts_features.py, tests/attention/test_attention_ts_mla_cp.py

Test selection gap: Context sliding/variable-window and FP8 Q128 swaps decode coverage lives in test files whose full bodies were not inspected.

GPU-related changes: comment `/bot run` and wait for `flashinfer-bot` to reply.

- default: validated gpu_required

Final: `gpu_required`. Changes softmax mask-tile selection in FMHA context/decode and MLA decode kernels (task cache words, SMEM packed range, FP8 swaps score masking); numerics need GPU execution.

Selected tests: `tests/attention/test_attention_ts_features.py`, `tests/attention/test_attention_ts_mla_cp.py`

### PR 9749

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9749) · [Demo #164](https://github.com/kangbintNV/flashinfer/pull/164)

Formal: **success / bot_response_found**. No-reply diagnostic: **command_missing**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9749#issuecomment-7028226027)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated gpu_required

Final: `gpu_required`. CUDA kernel change: MoE finalize Lamport store now accumulates top-k/shared-expert terms in fp32 and rounds once, altering device-side numerics in a multi-GPU all-reduce fusion path.

Selected tests: `tests/comm/test_trtllm_moe_allreduce_fusion_finalize.py`, `tests/comm/test_cake_moe_finalize_allreduce.py`

### PR 9858

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9858) · [Demo #165](https://github.com/kangbintNV/flashinfer/pull/165)

Formal: **failure / command_missing**. No-reply diagnostic: **command_missing**.

New FP8 page-64 split-reducer device program, binding variant with dynamic shared-memory opt-in, and host CTA/split planning change decode launches; bitwise O/LSE parity needs Blackwell execution.

Evidence: flashinfer/mla/cake_trtllm_mla_blackwell.py, tests/mla/test_cake_mla_fp8_page64_reduce.py

Suggested tests: tests/mla/test_cake_mla_fp8_page64_reduce.py

Test selection gap: tests/mla/test_cake_autotune_candidates_mla.py head-reduce additions not inspected in full, so not selected; H100 lane cannot execute sm_100a/sm_103a cases.

GPU-related changes: comment `/bot run` and wait for `flashinfer-bot` to reply.

- default: validated gpu_required

Final: `gpu_required`. New FP8 page-64 split-reducer device program, binding variant with dynamic shared-memory opt-in, and host CTA/split planning change decode launches; bitwise O/LSE parity needs Blackwell execution.

Selected tests: `tests/mla/test_cake_mla_fp8_page64_reduce.py`

### PR 9857

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9857) · [Demo #166](https://github.com/kangbintNV/flashinfer/pull/166)

Formal: **failure / command_missing**. No-reply diagnostic: **command_missing**.

New split-KV reducer kernel, binding dispatch and host split planning change launched MLA decode geometry and numerics; validation needs Blackwell execution.

Evidence: csrc/cake_trtllm_mla_blackwell/cake_trtllm_mla_blackwell_7d583eccd1e76da0e7bc_kernel.cu, flashinfer/mla/cake_trtllm_mla_blackwell.py, tests/mla/test_cake_mla_splitkv.py

Suggested tests: tests/mla/test_cake_mla_splitkv.py

Test selection gap: Binding-dependency assertion in tests/attention/test_trtllm_gen_mla.py not selected: file body unavailable; autotune candidate additions in _core.py uninspected.

GPU-related changes: comment `/bot run` and wait for `flashinfer-bot` to reply.

- default: validated gpu_required

Final: `gpu_required`. New split-KV reducer kernel, binding dispatch and host split planning change launched MLA decode geometry and numerics; validation needs Blackwell execution.

Selected tests: `tests/mla/test_cake_mla_splitkv.py`

### PR 9834

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9834) · [Demo #167](https://github.com/kangbintNV/flashinfer/pull/167)

Formal: **failure / command_missing**. No-reply diagnostic: **command_missing**.

Replaced Cake split-KV device programs, reducer shared-memory staging/launch config, and backend=auto split-KV offers; numerics, bulk copies and CUDA-graph replay need Blackwell GPU validation

Evidence: csrc/cake_trtllm_mla_blackwell/cake_trtllm_mla_blackwell_26168a31cc8a607d8a15_kernel.cu, flashinfer/mla/_core.py, tests/mla/test_cake_mla_splitkv.py

Suggested tests: tests/mla

Test selection gap: Split-KV GPU tests skip off SM100a/SM103a; CI lanes listed (A10G/T4/H100) cannot execute them, so kernel changes may run unvalidated

GPU-related changes: comment `/bot run` and wait for `flashinfer-bot` to reply.

- default: validated gpu_required

Final: `gpu_required`. Replaced Cake split-KV device programs, reducer shared-memory staging/launch config, and backend=auto split-KV offers; numerics, bulk copies and CUDA-graph replay need Blackwell GPU validation

Selected tests: `tests/mla`

### PR 9818

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9818) · [Demo #168](https://github.com/kangbintNV/flashinfer/pull/168)

Formal: **failure / bot_run_required_after_retry**. No-reply diagnostic: **bot_run_required_after_retry**.

Unable to reliably establish a CPU-only exemption after the default analysis and one minimal retry.

- default: Cannot establish a CPU-only exemption: changed-file patches are incomplete.
- minimal: Cannot establish a CPU-only exemption: changed-file patches are incomplete.

Comment `/bot run` or `/bot run tests/...` and wait for the internal bot response.

- default: Cannot establish a CPU-only exemption: changed-file patches are incomplete.
- minimal: Cannot establish a CPU-only exemption: changed-file patches are incomplete.

Final: `unknown`. Cannot establish a CPU-only exemption: changed-file patches are incomplete.

### PR 9358

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9358) · [Demo #169](https://github.com/kangbintNV/flashinfer/pull/169)

Formal: **success / docs_only**. No-reply diagnostic: **docs_only**.

All hunks edit docstrings/RST text (Returns types, LSE wording, RoPE REPL prompts, install claim); no kernel, dispatch, dtype or launch logic altered.

Evidence: flashinfer/cake_fused_qk_rope_fp8_append.py, docs/installation.rst, flashinfer/rope.py

- default: validated docs_only

Final: `docs_only`. All hunks edit docstrings/RST text (Returns types, LSE wording, RoPE REPL prompts, install claim); no kernel, dispatch, dtype or launch logic altered.

### PR 9332

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9332) · [Demo #170](https://github.com/kangbintNV/flashinfer/pull/170)

Formal: **failure / bot_run_required_after_retry**. No-reply diagnostic: **bot_run_required_after_retry**.

Unable to reliably establish a CPU-only exemption after the default analysis and one minimal retry.

- default: Cannot establish a CPU-only exemption: changed-file patches are incomplete.
- minimal: Cannot establish a CPU-only exemption: changed-file patches are incomplete.

Comment `/bot run` or `/bot run tests/...` and wait for the internal bot response.

- default: Cannot establish a CPU-only exemption: changed-file patches are incomplete.
- minimal: Cannot establish a CPU-only exemption: changed-file patches are incomplete.

Final: `unknown`. Cannot establish a CPU-only exemption: changed-file patches are incomplete.

### PR 9307

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9307) · [Demo #171](https://github.com/kangbintNV/flashinfer/pull/171)

Formal: **success / bot_response_found**. No-reply diagnostic: **bot_run_required_after_retry**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9307#issuecomment-6785807973)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: AI requested a file outside the supplied repository inventory
- minimal: Cannot establish a CPU-only exemption: changed-file patches are incomplete.

Final: `unknown`. Cannot establish a CPU-only exemption: changed-file patches are incomplete.

### PR 9545

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/9545) · [Demo #172](https://github.com/kangbintNV/flashinfer/pull/172)

Formal: **success / bot_response_found**. No-reply diagnostic: **docs_only**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/9545#issuecomment-6957693037)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: validated docs_only

Final: `docs_only`. Only comment text inside the TGV epilogue changed; fences, barrier order and generated kernel are byte-identical, so no GPU validation is implicated.

### PR 8464

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/8464) · [Demo #173](https://github.com/kangbintNV/flashinfer/pull/173)

Formal: **success / bot_response_found**. No-reply diagnostic: **bot_run_required_after_retry**.

[Internal bot response](https://github.com/flashinfer-ai/flashinfer/pull/8464#issuecomment-6659423942)

Source and LLM analysis skipped. Pipeline creation, result and commit correspondence are not evaluated.

The following analysis belongs only to the counterfactual diagnostic; formal analysis is skipped.

- default: AI requested a file outside the supplied repository inventory
- minimal: Inference Hub returned invalid JSON

Final: `unknown`. Inference Hub returned invalid JSON

### PR 8960

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/8960) · [Demo #174](https://github.com/kangbintNV/flashinfer/pull/174)

Formal: **success / docs_only**. No-reply diagnostic: **docs_only**.

Only Markdown/RST documentation changed.

Evidence: docs/training_backend_migration.md


Final: `docs_only`. Only Markdown/RST documentation changed.

### PR 8930

[Upstream](https://github.com/flashinfer-ai/flashinfer/pull/8930) · [Demo #175](https://github.com/kangbintNV/flashinfer/pull/175)

Formal: **success / docs_only**. No-reply diagnostic: **docs_only**.

Only Markdown/RST documentation changed.

Evidence: docs/training_backend_names.md


Final: `docs_only`. Only Markdown/RST documentation changed.

