# Bot Run Request Check：移除 experimental 豁免后的 150 PR 实验

固定检查器：[b53d126acf2ca62abff733af5525ebd522035750](https://github.com/flashinfer-ai/flashinfer/commit/b53d126acf2ca62abff733af5525ebd522035750)，PR #10020。

## 当前状态

原 100 个实验 PR 已更新，另建 50 个新实验 PR。已核对原始 diff/源码树、评论快照和全部 750 个检查器文件版本。已收集并核验完整原生结果：**150/150**。
Actions 已由用户恢复，本批通过真实 workflow_dispatch 执行。每个正式 Check 都核对 github-actions App、当前实验 head SHA、完成状态和结论；没有使用 commit status 替代。表中“运行中/排队中/未运行”表示尚未取得完整结果，不是 unknown。此前 fork 因 Actions 使用规模暂停的证据单独保留。

## 修正规则与验证

- 删除 experimental 目录快捷放行、模型 prompt 豁免和旧 experimental-only 分类缓存。GPU 改动无论是否 experimental，都需要有效内部回复；docs/CPU 仍按实际行为豁免。
- 历史内部回复仍有效，不要求 pipeline 启动/通过；公开 bot 回复不替代内部回复。原始回复缺席时才分析代码，失败/unknown 以 minimal 重试一次。
- 回归测试先复现 5 个失败断言；修正后 47 项 gate、66 项 infra 和 10 项 transport 测试通过，changed-file pre-commit 通过。
- 本地实时 #5658 预检已由 cpu_only 改为 gpu_required；它不是原生正式实验结果，不计入结果总数。
- 原 100 个样本和新增 50 个原 PR 无重复，另排除了保守排重清单中的其他历史原 PR。候选 #4903 因落地 diff 为空在推理前剔除，以 #2541 替换。
- 旧 50 中 8 个 PR 的原分支 head blob 与落地 merged blob 不同；21 个文件的净增删行均一致，原始冻结 files/comments 也完全保留。此为原有 merge-context 差异，本次未改写成一致；详见 legacy-blob-audit.json。所有 150 个源前后树及净改动均已核对。
- 静态审阅有两处复核更正：#9814 从 GPU 改为 CPU（仅 JSON 报告字段）；#7077 从 CPU 改为 GPU（同时移除了 GPU custom/fake-op 注册）。初判文件和更正证据均保留，实际模型输出/Check 结果未更改。
- “助手审阅未定”是静态审阅不能确定分类对错，与检查器 unknown 或运行状态不同；不是维护者人工标注。

## 汇总

```json
{
  "cohorts": {
    "old50": 50,
    "fresh50": 50,
    "new50": 50
  },
  "formal": {
    "success": 108,
    "failure": 42
  },
  "formal_assessment": {
    "correct_allow": 106,
    "pending_review": 6,
    "correct_block": 37,
    "false_block": 1,
    "false_allow": 0,
    "not_run": 0
  },
  "classifications": {
    "cpu_only": 18,
    "gpu_required": 93,
    "unknown": 13,
    "docs_only": 26
  },
  "classification_assessment": {
    "match": 124,
    "pending_review": 9,
    "analysis_failure": 13,
    "docs_cpu_label_difference": 3,
    "mismatch": 1
  },
  "native_formal_checks_verified": 150,
  "minimal_retry_cases": 21,
  "native_infrastructure_failures": 0,
  "source_integrity_verified": 150,
  "legacy_original_head_merged_blob_difference_prs": 8,
  "gpu_tests_started": 0,
  "bot_commands_posted": 0,
  "native_check_runs_verified": 224,
  "reply_samples": 74,
  "execution_states": {
    "completed": 150
  },
  "analysis_unknown_cases": 13,
  "formal_unknown_cases": 3,
  "shortcut_diagnostic_unknown_cases": 10,
  "minimal_retry_recovered": 8,
  "model_http_calls": 565,
  "temperature_compatibility_http400": 282,
  "baseline_formal_counts": {
    "success": 74,
    "failure": 26
  },
  "cohorts_detail": {
    "old50": {
      "formal": {
        "success": 39,
        "failure": 11
      },
      "classifications": {
        "cpu_only": 9,
        "gpu_required": 33,
        "unknown": 2,
        "docs_only": 6
      },
      "assessment": {
        "correct_allow": 38,
        "pending_review": 2,
        "correct_block": 10
      }
    },
    "fresh50": {
      "formal": {
        "success": 36,
        "failure": 14
      },
      "classifications": {
        "docs_only": 10,
        "cpu_only": 5,
        "gpu_required": 33,
        "unknown": 2
      },
      "assessment": {
        "correct_allow": 36,
        "correct_block": 10,
        "pending_review": 3,
        "false_block": 1
      }
    },
    "new50": {
      "formal": {
        "success": 33,
        "failure": 17
      },
      "classifications": {
        "docs_only": 10,
        "cpu_only": 4,
        "unknown": 9,
        "gpu_required": 27
      },
      "assessment": {
        "correct_allow": 32,
        "pending_review": 1,
        "correct_block": 17
      }
    }
  }
}
```

## 最终结论与误差统计

**150/150 实验完成，224 个原生 Check Run 已核验：150 个正式门禁 + 74 个独立无回复诊断。正式通过 108，失败 42。新增 50 个实验为 33 通过、17 失败；原 100 个为 75 通过、25 失败。**

以下“正确/错误”依据助手对实际 diff 的静态审阅，不是维护者人工金标。初始标签与两次复核更正保留，未改动任何模型输出或正式结论。

| 正式门禁评估 | 数量 | 含义 |
|---|---:|---|
| 正确放行 | 106 | 符合回复优先规则，或可确认的 docs/CPU 改动 |
| 正确阻塞 | 37 | 可确认 GPU 改动且没有有效内部回复，包括保守 unknown 阻塞 |
| 误放行 | 0 | 本次静态审阅未确认 GPU 无回复被放行；不等于证明不存在 |
| 误阻塞 | 1 | #8932：CPU 延迟导出/打包规则，文件请求校验失败后 unknown |
| 待确认 | 6 | 无回复且助手无法确定 CPU/GPU，不计入正确或误判 |

分类另外统计：124 个与审阅一致、3 个 docs/CPU 标签差异、1 个 CPU/GPU 分歧（#9478）、13 个分析失败/unknown、9 个审阅未定。9 个审阅未定中有 3 个因有效内部回复可确认正式放行符合规则，因此正式待确认只有 6 个。

| 分析/运行异常（与正式评估分开，不能相加） | 数量 |
|---|---:|
| 默认分析失败或不确定，启动一次 minimal 重试 | 21 |
| minimal 恢复成明确分类 | 8 |
| 两次分析后仍 unknown | 13 |
| unknown 的正式门禁（无回复，全部 failure） | 3 |
| unknown 的独立诊断（有回复，正式依策略 success） | 10 |
| 原生 workflow/check 无法取得有效终态的基础设施失败 | 0 |
| 已恢复的本地收集故障 | 1 |
| 已恢复的模型 HTTP 超时 | 1 |

13 个 unknown 均保留请求/响应：9 个止于文件请求校验，4 个止于 GPU 证据路径校验，没有隐去为 CPU。文件请求失败多与本次历史重放的上下文有关：固定的新检查器/可信 CI 引用了新位置，旧源树仍用 scripts/ 而不是 scripts/infra/，模型也请求了不在该历史快照内的文件。它证明这种历史输入组合下会 unknown，不能直接外推为当前 main 的同等失败率。

模型原始 HTTP 记录共 565 条：282 次 200、282 次 temperature 参数兼容性 400 后成功重发、1 次可恢复超时。这些传输层兼容重发不是额外的 minimal 推理重试。#9813 的 artifact 下载 TLS 故障由本地收集器恢复，未重跑该模型/工作流，也未改变检查器；详见 collector-download-incident.json。

## 代表案例与保留问题

- **experimental GPU 不再显示为 CPU：**[原 #5658](https://github.com/flashinfer-ai/flashinfer/pull/5658) / [实验 #204](https://github.com/kangbintNV/flashinfer/pull/204)，[分类诊断](https://github.com/kangbintNV/flashinfer/runs/139886700679)明确为 gpu_required/failure；[正式 Check](https://github.com/kangbintNV/flashinfer/runs/139886663294)因真实历史内部回复 success。这两个结果展示不同的判断步骤。
- **experimental 目录不再直接放行：**[原 #7077](https://github.com/flashinfer-ai/flashinfer/pull/7077) / [实验 #188](https://github.com/kangbintNV/flashinfer/pull/188)，[正式 Check](https://github.com/kangbintNV/flashinfer/runs/139942699848)由旧版本 experimental_only 放行变为 GPU 无回复失败。完整 diff 移除了 GPU forward/backward 包装的 custom/fake-op 注册，并非仅 CPU 导入测试。初始助手 CPU 标签错误，已保存复核原因。
- **unknown 无回复会阻塞：**[原 #8036](https://github.com/flashinfer-ai/flashinfer/pull/8036) / [实验 #239](https://github.com/kangbintNV/flashinfer/pull/239)、[原 #9679](https://github.com/flashinfer-ai/flashinfer/pull/9679) / [实验 #257](https://github.com/kangbintNV/flashinfer/pull/257)、[原 #8932](https://github.com/flashinfer-ai/flashinfer/pull/8932) / [实验 #223](https://github.com/kangbintNV/flashinfer/pull/223)的正式结果全部 failure。前两者静态审阅为 GPU，属于保守正确阻塞；#8932 是本批确认的误阻塞。
- **误阻塞复现：**[原 #8932](https://github.com/flashinfer-ai/flashinfer/pull/8932) / [实验 #223](https://github.com/kangbintNV/flashinfer/pull/223)只将现有 fused_moe 懒加载改为表驱动，并补充打包规则断言/说明；初始静态审阅已标 CPU。默认及 minimal 都请求历史树不存在的 scripts/infra/task_run_unit_tests.sh、scripts/infra/unit_test_runner.py，尚未完成分类就被校验拒绝。[正式 Check](https://github.com/kangbintNV/flashinfer/runs/139948700294)和 issues.json 保留完整证据。本批未修复 #10020。
- **CPU/GPU 分类分歧：**[原 #9478](https://github.com/flashinfer-ai/flashinfer/pull/9478) / [实验 #213](https://github.com/kangbintNV/flashinfer/pull/213)，诊断认为 gpu_required，助手预期 CPU。diff 仅按 Windows 选择 ucrtbase 获取 malloc/free；调用链用于 DLPack 的主机 _ViewBlock，GPU 指针/shape/dtype/launch 未改，主机分配/释放及导出结构可独立核对。模型担心 CUDA tensor view 生命周期，本批未实测 Windows，保留该静态审阅分歧。正式因历史回复通过，不能算分类正确。[分类诊断](https://github.com/kangbintNV/flashinfer/runs/139947682971)。
- **没有选出 case 仍识别 GPU：**[原 #9693](https://github.com/flashinfer-ai/flashinfer/pull/9693) / [实验 #216](https://github.com/kangbintNV/flashinfer/pull/216) 和 [原 #8815](https://github.com/flashinfer-ai/flashinfer/pull/8815) / [实验 #218](https://github.com/kangbintNV/flashinfer/pull/218) 的 selected targets=[]，仍为 gpu_required。前者改 persistent decode barrier，后者改 SM100 scale buffer 的 zero-fill；前者默认 target 校验失败、minimal 恢复 GPU，说明 target 校验仍会造成重试成本。旧版本曾见的 target 校验导致最终 unknown 的问题，在本次这两例未重现，不能宣称完全排除。
- **公开回复不能代替内部回复：**[原 #6458](https://github.com/flashinfer-ai/flashinfer/pull/6458) / [实验 #219](https://github.com/kangbintNV/flashinfer/pull/219) 的公开 bot 回复未获认可，正式 waiting_for_bot/failure。[正式 Check](https://github.com/kangbintNV/flashinfer/runs/139948130194)。
- **助手初判也会错：**[原 #9814](https://github.com/flashinfer-ai/flashinfer/pull/9814) / [实验 #148](https://github.com/kangbintNV/flashinfer/pull/148)仅改 benchmark JSON 报告 baseline_grid_ctas 字段，未改 kernel grid；模型 CPU 判定合理。初判 GPU 已更正并保留原标签，不计作模型误放行。

## unknown 逐例

GPU evidence validation 表示返回证据中包含未被允许的已读/差异/预算文件名路径；requested file validation 表示请求不在固定完整源树中的文件。所有原始响应与校验错误可在 evidence-traces.zip 查看。

| 原 PR | 正式结果 | 分类来源 | 最终失败点 |
|---|---|---|---|
| [#9989](https://github.com/flashinfer-ai/flashinfer/pull/9989) | [success](https://github.com/kangbintNV/flashinfer/runs/139893850246) | 独立无回复诊断 | gpu_evidence_validation |
| [#9991](https://github.com/flashinfer-ai/flashinfer/pull/9991) | [success](https://github.com/kangbintNV/flashinfer/runs/139894292574) | 独立无回复诊断 | gpu_evidence_validation |
| [#8433](https://github.com/flashinfer-ai/flashinfer/pull/8433) | [success](https://github.com/kangbintNV/flashinfer/runs/139948628562) | 独立无回复诊断 | requested_file_validation |
| [#8932](https://github.com/flashinfer-ai/flashinfer/pull/8932) | [failure](https://github.com/kangbintNV/flashinfer/runs/139948700294) | 正式无回复分析 | requested_file_validation |
| [#8036](https://github.com/flashinfer-ai/flashinfer/pull/8036) | [failure](https://github.com/kangbintNV/flashinfer/runs/139888155076) | 正式无回复分析 | requested_file_validation |
| [#8740](https://github.com/flashinfer-ai/flashinfer/pull/8740) | [success](https://github.com/kangbintNV/flashinfer/runs/139888471999) | 独立无回复诊断 | requested_file_validation |
| [#8479](https://github.com/flashinfer-ai/flashinfer/pull/8479) | [success](https://github.com/kangbintNV/flashinfer/runs/139888698666) | 独立无回复诊断 | requested_file_validation |
| [#5545](https://github.com/flashinfer-ai/flashinfer/pull/5545) | [success](https://github.com/kangbintNV/flashinfer/runs/139889392355) | 独立无回复诊断 | gpu_evidence_validation |
| [#9679](https://github.com/flashinfer-ai/flashinfer/pull/9679) | [failure](https://github.com/kangbintNV/flashinfer/runs/139890024071) | 正式无回复分析 | gpu_evidence_validation |
| [#9379](https://github.com/flashinfer-ai/flashinfer/pull/9379) | [success](https://github.com/kangbintNV/flashinfer/runs/139890638037) | 独立无回复诊断 | requested_file_validation |
| [#8002](https://github.com/flashinfer-ai/flashinfer/pull/8002) | [success](https://github.com/kangbintNV/flashinfer/runs/139890645042) | 独立无回复诊断 | requested_file_validation |
| [#9329](https://github.com/flashinfer-ai/flashinfer/pull/9329) | [success](https://github.com/kangbintNV/flashinfer/runs/139891528607) | 独立无回复诊断 | requested_file_validation |
| [#9493](https://github.com/flashinfer-ai/flashinfer/pull/9493) | [success](https://github.com/kangbintNV/flashinfer/runs/139891919978) | 独立无回复诊断 | requested_file_validation |

## 助手静态审阅待确认（不是 Checks 未运行）

以下 9 个案例均已真实执行完毕；缺的是对分类正确性的独立确认。保留原始未定标签，不拿模型自身答案当标准答案。

| 原 PR | 模型分类 | 正式结果 | 待确认原因 |
|---|---|---|---|
| [#10005](https://github.com/flashinfer-ai/flashinfer/pull/10005) | gpu_required | [failure](https://github.com/kangbintNV/flashinfer/runs/139893357949) | CI dependency constraint changes cuda-core binding selection. Confirm whether GPU-free environment/import validation suffices for the exact binding compatibility issue. |
| [#10006](https://github.com/flashinfer-ai/flashinfer/pull/10006) | cpu_only | [success](https://github.com/kangbintNV/flashinfer/runs/139893529200) | EP setup preserves newer NCCL wheels; effect on communication runtime compatibility versus bounded packaging behavior needs confirmation. |
| [#9843](https://github.com/flashinfer-ai/flashinfer/pull/9843) | gpu_required | [success](https://github.com/kangbintNV/flashinfer/runs/139897049996) | Test adjusts host SMEM over-capacity ring calculation and architecture skip. Need confirm GPU-free configuration validation versus actual device-dependent test requirements. |
| [#9681](https://github.com/flashinfer-ai/flashinfer/pull/9681) | gpu_required | [failure](https://github.com/kangbintNV/flashinfer/runs/139943969044) | One JIT object filename expression changes plus CPU Ninja-output tests. GPU-related build/load integration versus sufficient CPU path contract needs owner confirmation. |
| [#9481](https://github.com/flashinfer-ai/flashinfer/pull/9481) | gpu_required | [success](https://github.com/kangbintNV/flashinfer/runs/139943990668) | nvcc versus nvcc.exe compiler discovery changes in JIT; CPU path-selection coverage exists. Whether GPU build/run validation is needed needs owner confirmation. |
| [#9327](https://github.com/flashinfer-ai/flashinfer/pull/9327) | gpu_required | [success](https://github.com/kangbintNV/flashinfer/runs/139946576296) | Reuse of host compile-worker pools extends resource lifetimes; CPU lifetime tests exist, but retained CUDA-context/device-resource implications need owner confirmation. |
| [#7067](https://github.com/flashinfer-ai/flashinfer/pull/7067) | gpu_required | [failure](https://github.com/kangbintNV/flashinfer/runs/139948666361) | Stable wrapper defers experimental backend import and binding-cache configuration to first use. CPU import coverage exists; compiled binding lifetime implications need confirmation. |
| [#3827](https://github.com/flashinfer-ai/flashinfer/pull/3827) | gpu_required | [failure](https://github.com/kangbintNV/flashinfer/runs/139949327921) | The docs-titled PR also changes GegluTanh CPU enum/helper behavior. Current code consumes this in GEMM dimensions, but the pinned historical fused_moe/core.py does not show that consumer; GPU effect at this snapshot versus sufficient CPU utility tests needs owner confirmation. |
| [#9462](https://github.com/flashinfer-ai/flashinfer/pull/9462) | cpu_only | [success](https://github.com/kangbintNV/flashinfer/runs/139888076869) | New native Windows ARM64 wheel/JIT-provider driver and DLL layout validation; requires native build evidence to decide whether GPU-free validation sufficiently covers generated-provider integration. |

本批说明：检查器按固定证据发布原生 Checks，取消 experimental 快捷放行后可阻塞 GPU 无回复改动；unknown 也不会自动免测。它尚不能证明模型分类全面可靠，尤其历史文件位置与大文件证据校验仍有问题。**没有配置 required checks，未实际尝试合并，因此展示的是可作为合并门禁的 Check 结论，不能声称已验证仓库层面强制阻止合并。**

## 完整结果表

有内部回复时，“分类”来自独立无回复诊断；它不替代正式结论。正式结果及链接只取实际原生 Check Run。

| 原 PR | 实验 PR | 批次 | 内部回复 | 正式 Check | 分类 | minimal | 助手审阅预期 |
|---|---|---|---|---|---|---|---|
| [#9788](https://github.com/flashinfer-ai/flashinfer/pull/9788) | [#126](https://github.com/kangbintNV/flashinfer/pull/126) | old50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139892983107) | [CPU](https://github.com/kangbintNV/flashinfer/runs/139892983107) | — | CPU |
| [#10013](https://github.com/flashinfer-ai/flashinfer/pull/10013) | [#127](https://github.com/kangbintNV/flashinfer/pull/127) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/10013#issuecomment-7152368777) | [success](https://github.com/kangbintNV/flashinfer/runs/139893039972) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139893048229) | — | GPU |
| [#9731](https://github.com/flashinfer-ai/flashinfer/pull/9731) | [#128](https://github.com/kangbintNV/flashinfer/pull/128) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9731#issuecomment-7117140767) | [success](https://github.com/kangbintNV/flashinfer/runs/139893305042) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139893314343) | — | GPU |
| [#10005](https://github.com/flashinfer-ai/flashinfer/pull/10005) | [#129](https://github.com/kangbintNV/flashinfer/pull/129) | old50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139893357949) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139893357949) | — | 审阅未定 |
| [#10006](https://github.com/flashinfer-ai/flashinfer/pull/10006) | [#130](https://github.com/kangbintNV/flashinfer/pull/130) | old50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139893529200) | [CPU](https://github.com/kangbintNV/flashinfer/runs/139893529200) | — | 审阅未定 |
| [#9989](https://github.com/flashinfer-ai/flashinfer/pull/9989) | [#131](https://github.com/kangbintNV/flashinfer/pull/131) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9989#issuecomment-7141676310) | [success](https://github.com/kangbintNV/flashinfer/runs/139893850246) | [unknown](https://github.com/kangbintNV/flashinfer/runs/139893860250) | 有 | GPU |
| [#9990](https://github.com/flashinfer-ai/flashinfer/pull/9990) | [#132](https://github.com/kangbintNV/flashinfer/pull/132) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9990#issuecomment-7137423935) | [success](https://github.com/kangbintNV/flashinfer/runs/139893908776) | [CPU](https://github.com/kangbintNV/flashinfer/runs/139893914987) | — | CPU |
| [#9916](https://github.com/flashinfer-ai/flashinfer/pull/9916) | [#133](https://github.com/kangbintNV/flashinfer/pull/133) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9916#issuecomment-7119623448) | [success](https://github.com/kangbintNV/flashinfer/runs/139893888319) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139893897092) | — | GPU |
| [#9978](https://github.com/flashinfer-ai/flashinfer/pull/9978) | [#134](https://github.com/kangbintNV/flashinfer/pull/134) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9978#issuecomment-7130412330) | [success](https://github.com/kangbintNV/flashinfer/runs/139893902661) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139893910618) | — | GPU |
| [#9964](https://github.com/flashinfer-ai/flashinfer/pull/9964) | [#135](https://github.com/kangbintNV/flashinfer/pull/135) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9964#issuecomment-7131410753) | [success](https://github.com/kangbintNV/flashinfer/runs/139894230766) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139894266080) | — | GPU |
| [#9958](https://github.com/flashinfer-ai/flashinfer/pull/9958) | [#136](https://github.com/kangbintNV/flashinfer/pull/136) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9958#issuecomment-7122388075) | [success](https://github.com/kangbintNV/flashinfer/runs/139894265296) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139894275387) | — | GPU |
| [#9991](https://github.com/flashinfer-ai/flashinfer/pull/9991) | [#137](https://github.com/kangbintNV/flashinfer/pull/137) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9991#issuecomment-7137430127) | [success](https://github.com/kangbintNV/flashinfer/runs/139894292574) | [unknown](https://github.com/kangbintNV/flashinfer/runs/139894327628) | 有 | GPU |
| [#9817](https://github.com/flashinfer-ai/flashinfer/pull/9817) | [#138](https://github.com/kangbintNV/flashinfer/pull/138) | old50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139894318681) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139894318681) | — | GPU |
| [#9716](https://github.com/flashinfer-ai/flashinfer/pull/9716) | [#139](https://github.com/kangbintNV/flashinfer/pull/139) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9716#issuecomment-7119967898) | [success](https://github.com/kangbintNV/flashinfer/runs/139894921593) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139894932828) | 有 | GPU |
| [#9974](https://github.com/flashinfer-ai/flashinfer/pull/9974) | [#140](https://github.com/kangbintNV/flashinfer/pull/140) | old50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139894896397) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139894896397) | — | GPU |
| [#9892](https://github.com/flashinfer-ai/flashinfer/pull/9892) | [#141](https://github.com/kangbintNV/flashinfer/pull/141) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9892#issuecomment-7131921554) | [success](https://github.com/kangbintNV/flashinfer/runs/139894955328) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139894964930) | — | GPU |
| [#9885](https://github.com/flashinfer-ai/flashinfer/pull/9885) | [#142](https://github.com/kangbintNV/flashinfer/pull/142) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9885#issuecomment-7122274355) | [success](https://github.com/kangbintNV/flashinfer/runs/139895363058) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139895397913) | — | GPU |
| [#9651](https://github.com/flashinfer-ai/flashinfer/pull/9651) | [#143](https://github.com/kangbintNV/flashinfer/pull/143) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9651#issuecomment-7120452466) | [success](https://github.com/kangbintNV/flashinfer/runs/139895383373) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139895393999) | — | GPU |
| [#9876](https://github.com/flashinfer-ai/flashinfer/pull/9876) | [#144](https://github.com/kangbintNV/flashinfer/pull/144) | old50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139895409626) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139895409626) | — | GPU |
| [#9917](https://github.com/flashinfer-ai/flashinfer/pull/9917) | [#145](https://github.com/kangbintNV/flashinfer/pull/145) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9917#issuecomment-7118627807) | [success](https://github.com/kangbintNV/flashinfer/runs/139895745179) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139895754402) | — | GPU |
| [#9816](https://github.com/flashinfer-ai/flashinfer/pull/9816) | [#146](https://github.com/kangbintNV/flashinfer/pull/146) | old50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139895751616) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139895751616) | — | GPU |
| [#9815](https://github.com/flashinfer-ai/flashinfer/pull/9815) | [#147](https://github.com/kangbintNV/flashinfer/pull/147) | old50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139895774677) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139895774677) | — | GPU |
| [#9814](https://github.com/flashinfer-ai/flashinfer/pull/9814) | [#148](https://github.com/kangbintNV/flashinfer/pull/148) | old50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139896280576) | [CPU](https://github.com/kangbintNV/flashinfer/runs/139896280576) | — | CPU（[复核更正](static-review-corrections.json)） |
| [#9813](https://github.com/flashinfer-ai/flashinfer/pull/9813) | [#149](https://github.com/kangbintNV/flashinfer/pull/149) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9813#issuecomment-7073352142) | [success](https://github.com/kangbintNV/flashinfer/runs/139896294349) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139896303699) | — | GPU |
| [#9771](https://github.com/flashinfer-ai/flashinfer/pull/9771) | [#150](https://github.com/kangbintNV/flashinfer/pull/150) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9771#issuecomment-7093273577) | [success](https://github.com/kangbintNV/flashinfer/runs/139896328885) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139896365721) | — | GPU |
| [#9819](https://github.com/flashinfer-ai/flashinfer/pull/9819) | [#151](https://github.com/kangbintNV/flashinfer/pull/151) | old50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139896333416) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139896333416) | — | GPU |
| [#9908](https://github.com/flashinfer-ai/flashinfer/pull/9908) | [#152](https://github.com/kangbintNV/flashinfer/pull/152) | old50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139896691556) | [CPU](https://github.com/kangbintNV/flashinfer/runs/139896691556) | — | CPU |
| [#9897](https://github.com/flashinfer-ai/flashinfer/pull/9897) | [#153](https://github.com/kangbintNV/flashinfer/pull/153) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9897#issuecomment-7115181575) | [success](https://github.com/kangbintNV/flashinfer/runs/139896670588) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139896704166) | — | GPU |
| [#9844](https://github.com/flashinfer-ai/flashinfer/pull/9844) | [#154](https://github.com/kangbintNV/flashinfer/pull/154) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9844#issuecomment-7076553375) | [success](https://github.com/kangbintNV/flashinfer/runs/139896690275) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139896699240) | — | GPU |
| [#9843](https://github.com/flashinfer-ai/flashinfer/pull/9843) | [#155](https://github.com/kangbintNV/flashinfer/pull/155) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9843#issuecomment-7076551897) | [success](https://github.com/kangbintNV/flashinfer/runs/139897049996) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139897057951) | 有 | 审阅未定 |
| [#9694](https://github.com/flashinfer-ai/flashinfer/pull/9694) | [#156](https://github.com/kangbintNV/flashinfer/pull/156) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9694#issuecomment-7035450417) | [success](https://github.com/kangbintNV/flashinfer/runs/139898194966) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139898204597) | — | GPU |
| [#9847](https://github.com/flashinfer-ai/flashinfer/pull/9847) | [#157](https://github.com/kangbintNV/flashinfer/pull/157) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9847#issuecomment-7077462090) | [success](https://github.com/kangbintNV/flashinfer/runs/139938301869) | [CPU](https://github.com/kangbintNV/flashinfer/runs/139938341249) | — | CPU |
| [#9861](https://github.com/flashinfer-ai/flashinfer/pull/9861) | [#158](https://github.com/kangbintNV/flashinfer/pull/158) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9861#issuecomment-7094014552) | [success](https://github.com/kangbintNV/flashinfer/runs/139938329222) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139938340099) | — | GPU |
| [#9871](https://github.com/flashinfer-ai/flashinfer/pull/9871) | [#159](https://github.com/kangbintNV/flashinfer/pull/159) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9871#issuecomment-7102324850) | [success](https://github.com/kangbintNV/flashinfer/runs/139938411008) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139938421164) | — | GPU |
| [#9865](https://github.com/flashinfer-ai/flashinfer/pull/9865) | [#160](https://github.com/kangbintNV/flashinfer/pull/160) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9865#issuecomment-7093929737) | [success](https://github.com/kangbintNV/flashinfer/runs/139938375881) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139938384235) | — | GPU |
| [#9894](https://github.com/flashinfer-ai/flashinfer/pull/9894) | [#161](https://github.com/kangbintNV/flashinfer/pull/161) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9894#issuecomment-7106000551) | [success](https://github.com/kangbintNV/flashinfer/runs/139938407328) | [CPU](https://github.com/kangbintNV/flashinfer/runs/139938444933) | — | CPU |
| [#9836](https://github.com/flashinfer-ai/flashinfer/pull/9836) | [#162](https://github.com/kangbintNV/flashinfer/pull/162) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9836#issuecomment-7091022464) | [success](https://github.com/kangbintNV/flashinfer/runs/139938501777) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139938510234) | — | GPU |
| [#9846](https://github.com/flashinfer-ai/flashinfer/pull/9846) | [#163](https://github.com/kangbintNV/flashinfer/pull/163) | old50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139938487000) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139938487000) | — | GPU |
| [#9749](https://github.com/flashinfer-ai/flashinfer/pull/9749) | [#164](https://github.com/kangbintNV/flashinfer/pull/164) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9749#issuecomment-7028226027) | [success](https://github.com/kangbintNV/flashinfer/runs/139938503311) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139938513222) | — | GPU |
| [#9858](https://github.com/flashinfer-ai/flashinfer/pull/9858) | [#165](https://github.com/kangbintNV/flashinfer/pull/165) | old50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139939524759) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139939524759) | — | GPU |
| [#9857](https://github.com/flashinfer-ai/flashinfer/pull/9857) | [#166](https://github.com/kangbintNV/flashinfer/pull/166) | old50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139939557937) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139939557937) | — | GPU |
| [#9834](https://github.com/flashinfer-ai/flashinfer/pull/9834) | [#167](https://github.com/kangbintNV/flashinfer/pull/167) | old50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139939580876) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139939580876) | — | GPU |
| [#9818](https://github.com/flashinfer-ai/flashinfer/pull/9818) | [#168](https://github.com/kangbintNV/flashinfer/pull/168) | old50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139939611408) | [CPU](https://github.com/kangbintNV/flashinfer/runs/139939611408) | — | CPU |
| [#9358](https://github.com/flashinfer-ai/flashinfer/pull/9358) | [#169](https://github.com/kangbintNV/flashinfer/pull/169) | old50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139940177037) | [文档](https://github.com/kangbintNV/flashinfer/runs/139940177037) | — | 文档 |
| [#9332](https://github.com/flashinfer-ai/flashinfer/pull/9332) | [#170](https://github.com/kangbintNV/flashinfer/pull/170) | old50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139940198066) | [CPU](https://github.com/kangbintNV/flashinfer/runs/139940198066) | — | CPU |
| [#9307](https://github.com/flashinfer-ai/flashinfer/pull/9307) | [#171](https://github.com/kangbintNV/flashinfer/pull/171) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9307#issuecomment-6785807973) | [success](https://github.com/kangbintNV/flashinfer/runs/139940229188) | [文档](https://github.com/kangbintNV/flashinfer/runs/139940238779) | — | CPU |
| [#9545](https://github.com/flashinfer-ai/flashinfer/pull/9545) | [#172](https://github.com/kangbintNV/flashinfer/pull/172) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9545#issuecomment-6957693037) | [success](https://github.com/kangbintNV/flashinfer/runs/139940934015) | [文档](https://github.com/kangbintNV/flashinfer/runs/139940974162) | — | 文档 |
| [#8464](https://github.com/flashinfer-ai/flashinfer/pull/8464) | [#173](https://github.com/kangbintNV/flashinfer/pull/173) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8464#issuecomment-6659423942) | [success](https://github.com/kangbintNV/flashinfer/runs/139940973357) | [文档](https://github.com/kangbintNV/flashinfer/runs/139940982788) | 有 | 文档 |
| [#8960](https://github.com/flashinfer-ai/flashinfer/pull/8960) | [#174](https://github.com/kangbintNV/flashinfer/pull/174) | old50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139940923642) | [文档](https://github.com/kangbintNV/flashinfer/runs/139940923642) | — | 文档 |
| [#8930](https://github.com/flashinfer-ai/flashinfer/pull/8930) | [#175](https://github.com/kangbintNV/flashinfer/pull/175) | old50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139940946518) | [文档](https://github.com/kangbintNV/flashinfer/runs/139940946518) | — | 文档 |
| [#9369](https://github.com/flashinfer-ai/flashinfer/pull/9369) | [#176](https://github.com/kangbintNV/flashinfer/pull/176) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9369#issuecomment-6806129216) | [success](https://github.com/kangbintNV/flashinfer/runs/139940974154) | [文档](https://github.com/kangbintNV/flashinfer/runs/139941013356) | — | 文档 |
| [#9045](https://github.com/flashinfer-ai/flashinfer/pull/9045) | [#177](https://github.com/kangbintNV/flashinfer/pull/177) | fresh50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139941844109) | [文档](https://github.com/kangbintNV/flashinfer/runs/139941844109) | — | 文档 |
| [#7135](https://github.com/flashinfer-ai/flashinfer/pull/7135) | [#178](https://github.com/kangbintNV/flashinfer/pull/178) | fresh50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139941936315) | [文档](https://github.com/kangbintNV/flashinfer/runs/139941936315) | — | 文档 |
| [#4162](https://github.com/flashinfer-ai/flashinfer/pull/4162) | [#179](https://github.com/kangbintNV/flashinfer/pull/179) | fresh50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139941922472) | [文档](https://github.com/kangbintNV/flashinfer/runs/139941922472) | — | 文档 |
| [#6412](https://github.com/flashinfer-ai/flashinfer/pull/6412) | [#180](https://github.com/kangbintNV/flashinfer/pull/180) | fresh50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139941934788) | [文档](https://github.com/kangbintNV/flashinfer/runs/139941934788) | — | 文档 |
| [#3941](https://github.com/flashinfer-ai/flashinfer/pull/3941) | [#181](https://github.com/kangbintNV/flashinfer/pull/181) | fresh50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139941945627) | [文档](https://github.com/kangbintNV/flashinfer/runs/139941945627) | — | 文档 |
| [#9639](https://github.com/flashinfer-ai/flashinfer/pull/9639) | [#182](https://github.com/kangbintNV/flashinfer/pull/182) | fresh50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139941988776) | [CPU](https://github.com/kangbintNV/flashinfer/runs/139941988776) | — | CPU |
| [#9655](https://github.com/flashinfer-ai/flashinfer/pull/9655) | [#183](https://github.com/kangbintNV/flashinfer/pull/183) | fresh50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139942005273) | [CPU](https://github.com/kangbintNV/flashinfer/runs/139942005273) | — | CPU |
| [#9739](https://github.com/flashinfer-ai/flashinfer/pull/9739) | [#184](https://github.com/kangbintNV/flashinfer/pull/184) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9739#issuecomment-7026412299) | [success](https://github.com/kangbintNV/flashinfer/runs/139942594933) | [CPU](https://github.com/kangbintNV/flashinfer/runs/139942605778) | — | CPU |
| [#4945](https://github.com/flashinfer-ai/flashinfer/pull/4945) | [#185](https://github.com/kangbintNV/flashinfer/pull/185) | fresh50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139942622152) | [CPU](https://github.com/kangbintNV/flashinfer/runs/139942622152) | — | CPU |
| [#5383](https://github.com/flashinfer-ai/flashinfer/pull/5383) | [#186](https://github.com/kangbintNV/flashinfer/pull/186) | fresh50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139942634470) | [文档](https://github.com/kangbintNV/flashinfer/runs/139942634470) | — | CPU |
| [#9465](https://github.com/flashinfer-ai/flashinfer/pull/9465) | [#187](https://github.com/kangbintNV/flashinfer/pull/187) | fresh50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139942657212) | [CPU](https://github.com/kangbintNV/flashinfer/runs/139942657212) | — | CPU |
| [#7077](https://github.com/flashinfer-ai/flashinfer/pull/7077) | [#188](https://github.com/kangbintNV/flashinfer/pull/188) | fresh50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139942699848) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139942699848) | — | GPU（[复核更正](static-review-corrections.json)） |
| [#8561](https://github.com/flashinfer-ai/flashinfer/pull/8561) | [#189](https://github.com/kangbintNV/flashinfer/pull/189) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8561#issuecomment-6661899364) | [success](https://github.com/kangbintNV/flashinfer/runs/139942705022) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139942740406) | — | GPU |
| [#9200](https://github.com/flashinfer-ai/flashinfer/pull/9200) | [#190](https://github.com/kangbintNV/flashinfer/pull/190) | fresh50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139943137811) | [文档](https://github.com/kangbintNV/flashinfer/runs/139943137811) | — | 文档 |
| [#7653](https://github.com/flashinfer-ai/flashinfer/pull/7653) | [#191](https://github.com/kangbintNV/flashinfer/pull/191) | fresh50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139943161427) | [文档](https://github.com/kangbintNV/flashinfer/runs/139943161427) | — | 文档 |
| [#9681](https://github.com/flashinfer-ai/flashinfer/pull/9681) | [#192](https://github.com/kangbintNV/flashinfer/pull/192) | fresh50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139943969044) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139943969044) | — | 审阅未定 |
| [#9481](https://github.com/flashinfer-ai/flashinfer/pull/9481) | [#193](https://github.com/kangbintNV/flashinfer/pull/193) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9481#issuecomment-6905895364) | [success](https://github.com/kangbintNV/flashinfer/runs/139943990668) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139943999382) | — | 审阅未定 |
| [#9738](https://github.com/flashinfer-ai/flashinfer/pull/9738) | [#194](https://github.com/kangbintNV/flashinfer/pull/194) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9738#issuecomment-7025271294) | [success](https://github.com/kangbintNV/flashinfer/runs/139944010931) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139944020504) | — | GPU |
| [#9395](https://github.com/flashinfer-ai/flashinfer/pull/9395) | [#195](https://github.com/kangbintNV/flashinfer/pull/195) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9395#issuecomment-7132488096) | [success](https://github.com/kangbintNV/flashinfer/runs/139944044764) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139944053044) | — | GPU |
| [#9706](https://github.com/flashinfer-ai/flashinfer/pull/9706) | [#196](https://github.com/kangbintNV/flashinfer/pull/196) | fresh50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139944070575) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139944070575) | — | GPU |
| [#9669](https://github.com/flashinfer-ai/flashinfer/pull/9669) | [#197](https://github.com/kangbintNV/flashinfer/pull/197) | fresh50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139944104284) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139944104284) | — | GPU |
| [#9375](https://github.com/flashinfer-ai/flashinfer/pull/9375) | [#198](https://github.com/kangbintNV/flashinfer/pull/198) | fresh50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139944138564) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139944138564) | — | GPU |
| [#10036](https://github.com/flashinfer-ai/flashinfer/pull/10036) | [#199](https://github.com/kangbintNV/flashinfer/pull/199) | fresh50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139944440345) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139944440345) | 有 | GPU |
| [#9659](https://github.com/flashinfer-ai/flashinfer/pull/9659) | [#200](https://github.com/kangbintNV/flashinfer/pull/200) | fresh50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139945499823) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139945499823) | — | GPU |
| [#9649](https://github.com/flashinfer-ai/flashinfer/pull/9649) | [#201](https://github.com/kangbintNV/flashinfer/pull/201) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9649#issuecomment-7029324566) | [success](https://github.com/kangbintNV/flashinfer/runs/139945498024) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139945536054) | — | GPU |
| [#9949](https://github.com/flashinfer-ai/flashinfer/pull/9949) | [#202](https://github.com/kangbintNV/flashinfer/pull/202) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9949#issuecomment-7181797949) | [success](https://github.com/kangbintNV/flashinfer/runs/139945476915) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139945517287) | — | GPU |
| [#9550](https://github.com/flashinfer-ai/flashinfer/pull/9550) | [#203](https://github.com/kangbintNV/flashinfer/pull/203) | fresh50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139945504095) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139945504095) | 有 | GPU |
| [#5658](https://github.com/flashinfer-ai/flashinfer/pull/5658) | [#204](https://github.com/kangbintNV/flashinfer/pull/204) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/5658#issuecomment-5880412590) | [success](https://github.com/kangbintNV/flashinfer/runs/139886663294) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139886700679) | — | GPU |
| [#8081](https://github.com/flashinfer-ai/flashinfer/pull/8081) | [#205](https://github.com/kangbintNV/flashinfer/pull/205) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8081#issuecomment-6880608414) | [success](https://github.com/kangbintNV/flashinfer/runs/139945539826) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139945550958) | 有 | GPU |
| [#6711](https://github.com/flashinfer-ai/flashinfer/pull/6711) | [#206](https://github.com/kangbintNV/flashinfer/pull/206) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/6711#issuecomment-6974039523) | [success](https://github.com/kangbintNV/flashinfer/runs/139945560396) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139945570785) | — | GPU |
| [#9554](https://github.com/flashinfer-ai/flashinfer/pull/9554) | [#207](https://github.com/kangbintNV/flashinfer/pull/207) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9554#issuecomment-7076077410) | [success](https://github.com/kangbintNV/flashinfer/runs/139945608507) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139945619089) | — | GPU |
| [#8766](https://github.com/flashinfer-ai/flashinfer/pull/8766) | [#208](https://github.com/kangbintNV/flashinfer/pull/208) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8766#issuecomment-6983034862) | [success](https://github.com/kangbintNV/flashinfer/runs/139945919511) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139945929385) | — | GPU |
| [#6160](https://github.com/flashinfer-ai/flashinfer/pull/6160) | [#209](https://github.com/kangbintNV/flashinfer/pull/209) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/6160#issuecomment-7031181649) | [success](https://github.com/kangbintNV/flashinfer/runs/139946560988) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139946569870) | — | GPU |
| [#9327](https://github.com/flashinfer-ai/flashinfer/pull/9327) | [#210](https://github.com/kangbintNV/flashinfer/pull/210) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9327#issuecomment-6783825712) | [success](https://github.com/kangbintNV/flashinfer/runs/139946576296) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139946586976) | — | 审阅未定 |
| [#9289](https://github.com/flashinfer-ai/flashinfer/pull/9289) | [#211](https://github.com/kangbintNV/flashinfer/pull/211) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9289#issuecomment-7014293371) | [success](https://github.com/kangbintNV/flashinfer/runs/139946638329) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139946650192) | — | GPU |
| [#1163](https://github.com/flashinfer-ai/flashinfer/pull/1163) | [#212](https://github.com/kangbintNV/flashinfer/pull/212) | fresh50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139947606112) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139947606112) | — | GPU |
| [#9478](https://github.com/flashinfer-ai/flashinfer/pull/9478) | [#213](https://github.com/kangbintNV/flashinfer/pull/213) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9478#issuecomment-6981486445) | [success](https://github.com/kangbintNV/flashinfer/runs/139947640376) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139947682971) | — | CPU |
| [#8889](https://github.com/flashinfer-ai/flashinfer/pull/8889) | [#214](https://github.com/kangbintNV/flashinfer/pull/214) | fresh50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139947629631) | [文档](https://github.com/kangbintNV/flashinfer/runs/139947629631) | — | 文档 |
| [#9765](https://github.com/flashinfer-ai/flashinfer/pull/9765) | [#215](https://github.com/kangbintNV/flashinfer/pull/215) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9765#issuecomment-7034104120) | [success](https://github.com/kangbintNV/flashinfer/runs/139947652276) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139947692897) | — | GPU |
| [#9693](https://github.com/flashinfer-ai/flashinfer/pull/9693) | [#216](https://github.com/kangbintNV/flashinfer/pull/216) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9693#issuecomment-7001872107) | [success](https://github.com/kangbintNV/flashinfer/runs/139947682437) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139947691807) | 有 | GPU |
| [#9687](https://github.com/flashinfer-ai/flashinfer/pull/9687) | [#217](https://github.com/kangbintNV/flashinfer/pull/217) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9687#issuecomment-7010123047) | [success](https://github.com/kangbintNV/flashinfer/runs/139947709208) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139947720917) | — | GPU |
| [#8815](https://github.com/flashinfer-ai/flashinfer/pull/8815) | [#218](https://github.com/kangbintNV/flashinfer/pull/218) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8815#issuecomment-7020741789) | [success](https://github.com/kangbintNV/flashinfer/runs/139947735000) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139947775802) | — | GPU |
| [#6458](https://github.com/flashinfer-ai/flashinfer/pull/6458) | [#219](https://github.com/kangbintNV/flashinfer/pull/219) | fresh50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139948130194) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139948130194) | — | GPU |
| [#9640](https://github.com/flashinfer-ai/flashinfer/pull/9640) | [#220](https://github.com/kangbintNV/flashinfer/pull/220) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9640#issuecomment-6969555053) | [success](https://github.com/kangbintNV/flashinfer/runs/139948596942) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139948606582) | — | GPU |
| [#8433](https://github.com/flashinfer-ai/flashinfer/pull/8433) | [#221](https://github.com/kangbintNV/flashinfer/pull/221) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8433#issuecomment-6624366719) | [success](https://github.com/kangbintNV/flashinfer/runs/139948628562) | [unknown](https://github.com/kangbintNV/flashinfer/runs/139948638945) | 有 | GPU |
| [#7067](https://github.com/flashinfer-ai/flashinfer/pull/7067) | [#222](https://github.com/kangbintNV/flashinfer/pull/222) | fresh50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139948666361) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139948666361) | — | 审阅未定 |
| [#8932](https://github.com/flashinfer-ai/flashinfer/pull/8932) | [#223](https://github.com/kangbintNV/flashinfer/pull/223) | fresh50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139948700294) | [unknown](https://github.com/kangbintNV/flashinfer/runs/139948700294) | 有 | CPU |
| [#7819](https://github.com/flashinfer-ai/flashinfer/pull/7819) | [#224](https://github.com/kangbintNV/flashinfer/pull/224) | fresh50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139949222375) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139949222375) | — | GPU |
| [#3827](https://github.com/flashinfer-ai/flashinfer/pull/3827) | [#225](https://github.com/kangbintNV/flashinfer/pull/225) | fresh50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139949327921) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139949327921) | — | 审阅未定 |
| [#9082](https://github.com/flashinfer-ai/flashinfer/pull/9082) | [#228](https://github.com/kangbintNV/flashinfer/pull/228) | new50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139887403944) | [文档](https://github.com/kangbintNV/flashinfer/runs/139887403944) | — | 文档 |
| [#4948](https://github.com/flashinfer-ai/flashinfer/pull/4948) | [#229](https://github.com/kangbintNV/flashinfer/pull/229) | new50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139887456354) | [文档](https://github.com/kangbintNV/flashinfer/runs/139887456354) | — | 文档 |
| [#8185](https://github.com/flashinfer-ai/flashinfer/pull/8185) | [#230](https://github.com/kangbintNV/flashinfer/pull/230) | new50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139887447382) | [文档](https://github.com/kangbintNV/flashinfer/runs/139887447382) | — | 文档 |
| [#2541](https://github.com/flashinfer-ai/flashinfer/pull/2541) | [#231](https://github.com/kangbintNV/flashinfer/pull/231) | new50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139887463627) | [文档](https://github.com/kangbintNV/flashinfer/runs/139887463627) | — | 文档 |
| [#4175](https://github.com/flashinfer-ai/flashinfer/pull/4175) | [#232](https://github.com/kangbintNV/flashinfer/pull/232) | new50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139887550649) | [文档](https://github.com/kangbintNV/flashinfer/runs/139887550649) | — | 文档 |
| [#3710](https://github.com/flashinfer-ai/flashinfer/pull/3710) | [#233](https://github.com/kangbintNV/flashinfer/pull/233) | new50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139887500847) | [文档](https://github.com/kangbintNV/flashinfer/runs/139887500847) | — | 文档 |
| [#9985](https://github.com/flashinfer-ai/flashinfer/pull/9985) | [#234](https://github.com/kangbintNV/flashinfer/pull/234) | new50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139887530662) | [CPU](https://github.com/kangbintNV/flashinfer/runs/139887530662) | — | CPU |
| [#3853](https://github.com/flashinfer-ai/flashinfer/pull/3853) | [#235](https://github.com/kangbintNV/flashinfer/pull/235) | new50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139887543040) | [文档](https://github.com/kangbintNV/flashinfer/runs/139887543040) | — | CPU |
| [#9688](https://github.com/flashinfer-ai/flashinfer/pull/9688) | [#236](https://github.com/kangbintNV/flashinfer/pull/236) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9688#issuecomment-7001181982) | [success](https://github.com/kangbintNV/flashinfer/runs/139888050722) | [CPU](https://github.com/kangbintNV/flashinfer/runs/139888059103) | — | CPU |
| [#9462](https://github.com/flashinfer-ai/flashinfer/pull/9462) | [#237](https://github.com/kangbintNV/flashinfer/pull/237) | new50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139888076869) | [CPU](https://github.com/kangbintNV/flashinfer/runs/139888076869) | — | 审阅未定 |
| [#7625](https://github.com/flashinfer-ai/flashinfer/pull/7625) | [#238](https://github.com/kangbintNV/flashinfer/pull/238) | new50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139888095573) | [文档](https://github.com/kangbintNV/flashinfer/runs/139888095573) | — | 文档 |
| [#8036](https://github.com/flashinfer-ai/flashinfer/pull/8036) | [#239](https://github.com/kangbintNV/flashinfer/pull/239) | new50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139888155076) | [unknown](https://github.com/kangbintNV/flashinfer/runs/139888155076) | 有 | GPU |
| [#9656](https://github.com/flashinfer-ai/flashinfer/pull/9656) | [#240](https://github.com/kangbintNV/flashinfer/pull/240) | new50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139888142889) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139888142889) | — | GPU |
| [#8867](https://github.com/flashinfer-ai/flashinfer/pull/8867) | [#241](https://github.com/kangbintNV/flashinfer/pull/241) | new50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139888160375) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139888160375) | — | GPU |
| [#6902](https://github.com/flashinfer-ai/flashinfer/pull/6902) | [#242](https://github.com/kangbintNV/flashinfer/pull/242) | new50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139888174603) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139888174603) | — | GPU |
| [#5040](https://github.com/flashinfer-ai/flashinfer/pull/5040) | [#243](https://github.com/kangbintNV/flashinfer/pull/243) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/5040#issuecomment-5610482618) | [success](https://github.com/kangbintNV/flashinfer/runs/139888451533) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139888486012) | — | GPU |
| [#8740](https://github.com/flashinfer-ai/flashinfer/pull/8740) | [#245](https://github.com/kangbintNV/flashinfer/pull/245) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8740#issuecomment-6759578978) | [success](https://github.com/kangbintNV/flashinfer/runs/139888471999) | [unknown](https://github.com/kangbintNV/flashinfer/runs/139888484104) | 有 | GPU |
| [#8479](https://github.com/flashinfer-ai/flashinfer/pull/8479) | [#247](https://github.com/kangbintNV/flashinfer/pull/247) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8479#issuecomment-6813765933) | [success](https://github.com/kangbintNV/flashinfer/runs/139888698666) | [unknown](https://github.com/kangbintNV/flashinfer/runs/139888733199) | 有 | GPU |
| [#6790](https://github.com/flashinfer-ai/flashinfer/pull/6790) | [#248](https://github.com/kangbintNV/flashinfer/pull/248) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/6790#issuecomment-6325133828) | [success](https://github.com/kangbintNV/flashinfer/runs/139889001601) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139889009959) | — | GPU |
| [#9773](https://github.com/flashinfer-ai/flashinfer/pull/9773) | [#249](https://github.com/kangbintNV/flashinfer/pull/249) | new50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139889019675) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139889019675) | — | GPU |
| [#9660](https://github.com/flashinfer-ai/flashinfer/pull/9660) | [#250](https://github.com/kangbintNV/flashinfer/pull/250) | new50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139889039861) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139889039861) | — | GPU |
| [#10046](https://github.com/flashinfer-ai/flashinfer/pull/10046) | [#251](https://github.com/kangbintNV/flashinfer/pull/251) | new50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139889360345) | [CPU](https://github.com/kangbintNV/flashinfer/runs/139889360345) | — | CPU |
| [#6436](https://github.com/flashinfer-ai/flashinfer/pull/6436) | [#252](https://github.com/kangbintNV/flashinfer/pull/252) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/6436#issuecomment-6760153229) | [success](https://github.com/kangbintNV/flashinfer/runs/139889373406) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139889382617) | — | GPU |
| [#5545](https://github.com/flashinfer-ai/flashinfer/pull/5545) | [#253](https://github.com/kangbintNV/flashinfer/pull/253) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/5545#issuecomment-5850911673) | [success](https://github.com/kangbintNV/flashinfer/runs/139889392355) | [unknown](https://github.com/kangbintNV/flashinfer/runs/139889401889) | 有 | GPU |
| [#9112](https://github.com/flashinfer-ai/flashinfer/pull/9112) | [#254](https://github.com/kangbintNV/flashinfer/pull/254) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9112#issuecomment-7169436156) | [success](https://github.com/kangbintNV/flashinfer/runs/139889650961) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139889659148) | — | GPU |
| [#9468](https://github.com/flashinfer-ai/flashinfer/pull/9468) | [#255](https://github.com/kangbintNV/flashinfer/pull/255) | new50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139889686513) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139889686513) | — | GPU |
| [#9654](https://github.com/flashinfer-ai/flashinfer/pull/9654) | [#256](https://github.com/kangbintNV/flashinfer/pull/256) | new50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139890048376) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139890048376) | — | GPU |
| [#9679](https://github.com/flashinfer-ai/flashinfer/pull/9679) | [#257](https://github.com/kangbintNV/flashinfer/pull/257) | new50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139890024071) | [unknown](https://github.com/kangbintNV/flashinfer/runs/139890024071) | 有 | GPU |
| [#9464](https://github.com/flashinfer-ai/flashinfer/pull/9464) | [#258](https://github.com/kangbintNV/flashinfer/pull/258) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9464#issuecomment-6981793114) | [success](https://github.com/kangbintNV/flashinfer/runs/139890036513) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139890044688) | — | GPU |
| [#9745](https://github.com/flashinfer-ai/flashinfer/pull/9745) | [#259](https://github.com/kangbintNV/flashinfer/pull/259) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9745#issuecomment-7031186743) | [success](https://github.com/kangbintNV/flashinfer/runs/139890264928) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139890272717) | — | GPU |
| [#9379](https://github.com/flashinfer-ai/flashinfer/pull/9379) | [#260](https://github.com/kangbintNV/flashinfer/pull/260) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9379#issuecomment-6842701998) | [success](https://github.com/kangbintNV/flashinfer/runs/139890638037) | [unknown](https://github.com/kangbintNV/flashinfer/runs/139890646691) | 有 | GPU |
| [#8002](https://github.com/flashinfer-ai/flashinfer/pull/8002) | [#261](https://github.com/kangbintNV/flashinfer/pull/261) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8002#issuecomment-6610367880) | [success](https://github.com/kangbintNV/flashinfer/runs/139890645042) | [unknown](https://github.com/kangbintNV/flashinfer/runs/139890654321) | 有 | GPU |
| [#9463](https://github.com/flashinfer-ai/flashinfer/pull/9463) | [#262](https://github.com/kangbintNV/flashinfer/pull/262) | new50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139890675471) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139890675471) | — | GPU |
| [#9779](https://github.com/flashinfer-ai/flashinfer/pull/9779) | [#263](https://github.com/kangbintNV/flashinfer/pull/263) | new50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139890686235) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139890686235) | — | GPU |
| [#9628](https://github.com/flashinfer-ai/flashinfer/pull/9628) | [#264](https://github.com/kangbintNV/flashinfer/pull/264) | new50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139890948393) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139890948393) | 有 | GPU |
| [#8131](https://github.com/flashinfer-ai/flashinfer/pull/8131) | [#265](https://github.com/kangbintNV/flashinfer/pull/265) | new50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139890962192) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139890962192) | — | GPU |
| [#9676](https://github.com/flashinfer-ai/flashinfer/pull/9676) | [#266](https://github.com/kangbintNV/flashinfer/pull/266) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9676#issuecomment-7020916382) | [success](https://github.com/kangbintNV/flashinfer/runs/139891322890) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139891330941) | — | GPU |
| [#9329](https://github.com/flashinfer-ai/flashinfer/pull/9329) | [#267](https://github.com/kangbintNV/flashinfer/pull/267) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9329#issuecomment-6881712313) | [success](https://github.com/kangbintNV/flashinfer/runs/139891528607) | [unknown](https://github.com/kangbintNV/flashinfer/runs/139891537601) | 有 | GPU |
| [#9677](https://github.com/flashinfer-ai/flashinfer/pull/9677) | [#268](https://github.com/kangbintNV/flashinfer/pull/268) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9677#issuecomment-7022787743) | [success](https://github.com/kangbintNV/flashinfer/runs/139891542048) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139891550788) | — | GPU |
| [#9493](https://github.com/flashinfer-ai/flashinfer/pull/9493) | [#269](https://github.com/kangbintNV/flashinfer/pull/269) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9493#issuecomment-6911100042) | [success](https://github.com/kangbintNV/flashinfer/runs/139891919978) | [unknown](https://github.com/kangbintNV/flashinfer/runs/139891954821) | 有 | GPU |
| [#935](https://github.com/flashinfer-ai/flashinfer/pull/935) | [#270](https://github.com/kangbintNV/flashinfer/pull/270) | new50 | 无 | [success](https://github.com/kangbintNV/flashinfer/runs/139891931327) | [文档](https://github.com/kangbintNV/flashinfer/runs/139891931327) | — | 文档 |
| [#9967](https://github.com/flashinfer-ai/flashinfer/pull/9967) | [#271](https://github.com/kangbintNV/flashinfer/pull/271) | new50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139891954770) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139891954770) | — | GPU |
| [#9757](https://github.com/flashinfer-ai/flashinfer/pull/9757) | [#272](https://github.com/kangbintNV/flashinfer/pull/272) | new50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139891980309) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139891980309) | — | GPU |
| [#5629](https://github.com/flashinfer-ai/flashinfer/pull/5629) | [#273](https://github.com/kangbintNV/flashinfer/pull/273) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/5629#issuecomment-5865016332) | [success](https://github.com/kangbintNV/flashinfer/runs/139892007589) | [文档](https://github.com/kangbintNV/flashinfer/runs/139892016428) | — | 文档 |
| [#9998](https://github.com/flashinfer-ai/flashinfer/pull/9998) | [#274](https://github.com/kangbintNV/flashinfer/pull/274) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9998#issuecomment-7169964271) | [success](https://github.com/kangbintNV/flashinfer/runs/139892263354) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139892273924) | — | GPU |
| [#9848](https://github.com/flashinfer-ai/flashinfer/pull/9848) | [#275](https://github.com/kangbintNV/flashinfer/pull/275) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9848#issuecomment-7144687059) | [success](https://github.com/kangbintNV/flashinfer/runs/139892593886) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139892604078) | — | GPU |
| [#9725](https://github.com/flashinfer-ai/flashinfer/pull/9725) | [#276](https://github.com/kangbintNV/flashinfer/pull/276) | new50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139892609918) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139892609918) | — | GPU |
| [#9663](https://github.com/flashinfer-ai/flashinfer/pull/9663) | [#277](https://github.com/kangbintNV/flashinfer/pull/277) | new50 | 无 | [failure](https://github.com/kangbintNV/flashinfer/runs/139892632363) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139892632363) | — | GPU |
| [#9429](https://github.com/flashinfer-ai/flashinfer/pull/9429) | [#278](https://github.com/kangbintNV/flashinfer/pull/278) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9429#issuecomment-6926082806) | [success](https://github.com/kangbintNV/flashinfer/runs/139892648706) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139892658174) | — | GPU |
| [#8549](https://github.com/flashinfer-ai/flashinfer/pull/8549) | [#279](https://github.com/kangbintNV/flashinfer/pull/279) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8549#issuecomment-6941072903) | [success](https://github.com/kangbintNV/flashinfer/runs/139892952888) | [GPU](https://github.com/kangbintNV/flashinfer/runs/139892963324) | — | GPU |

## 能证明与不能证明

原生结果用于验证固定代码、冻结证据下的门禁判断、分类/重试输出及 GitHub Check 发布。工作流自身成功仅表示实验完成，不代表正式 Bot Run Request Check 通过；GPU 无回复的正式失败是预期结果。
本批不证明 GPU 数值/性能正确、用例覆盖充分、真实 bot 服务健康或当前 commit 实际已测试。未配置 required check/branch protection，不能声称已验证强制合并阻塞。新鲜模型响应非确定，本次不是严格的单变量因果 A/B。
代理没有修改 fork main 或仓库设置；运行中观察到 fork main 被其他活动更新，已另存观察记录，未覆盖或恢复该分支。

## 数据

[CSV](results.csv) · [完整 JSON](results.json) · [助手静态审阅](manual-review.json) · [初始审阅](manual-review-initial.json) · [复核更正](static-review-corrections.json) · [源码审计](source-audit.json) · [检查器版本](checker-pins.json) · [旧样本 merge-context 差异](legacy-blob-audit.json)
