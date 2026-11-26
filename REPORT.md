# Bot Run Request Check：50 个全新 merged PR 实验

固定检查器：`2f9840349e97effbb89737a6332673f490629094`。模型：`azure/anthropic/claude-opus-5`，精简 JSON；默认推理，失败/unknown 后 minimal 重试一次。

## 先说明平台限制

本批已创建 50 个全新 fork 实验 PR，完成真实 `run_pr` 入口重放，并发布 50 个正式 GitHub commit status 和 23 个独立分类诊断 status。它们显示在 PR 的状态检查列表（Checks/statusCheckRollup）并带 Details 链接。**它们不是原生 GitHub App Check Run，也没有实际 Actions 实验 run。**
fork 的 workflow dispatch 明确返回 `Actions has been disabled for this repository` (HTTP 422)；只读 permissions 查询却返回 enabled=true，平台状态存在不一致，根因未核实。当前 OAuth token 创建原生 Check Run 返回 `You must authenticate via a GitHub App` (HTTP 403)，与 [GitHub Checks API 的凭据要求](https://docs.github.com/en/rest/checks/runs#create-a-check-run) 一致。未修改设置、main、branch protection，未合并任何 PR。也因此本批不能证明 Actions 自动触发或 required-check 合并强制执行。

## 结果统计

- 正式：38 通过，12 失败；有原始内部回复 23 个，无回复 27 个。
- 人工对照正式策略：正确放行 38；正确判需阻塞 9；误放行 0；误阻塞 0；待确认 3。
- 正式路径模型失败 0；独立分类诊断模型失败 3；逐例执行/状态发布基础设施失败 0；全局 Actions/原生 Check 平台障碍 1 项。
- 分类（有回复时来自单独诊断，未覆盖正式结果）：{'docs_only': 8, 'cpu_only': 8, 'experimental_only': 4, 'gpu_required': 27, 'unknown': 3}。人工分类对照：{'match': 41, 'pending_manual': 5, 'mismatch': 1, 'model_failure': 3}。
- minimal 分析重试 5 例，恢复 2 例；另有 HTTP temperature 参数兼容重试 83 次，属于固定实现的传输兼容处理，不是额外 minimal 分析重试。
- 旧 run artifact 的 50 个原 PR 和已有实验均已排除；本批原 PR 零重复。逐 PR 源文件路径、Git blob/status 和评论快照 hash 均 50/50 一致。
- 待确认的边界为 #9681、#9481、#9327、#7067、#3827；其中 #9681/#7067/#3827 的正式阻塞也保留为待确认，不为它们强行标注正确或错误。

## 具体问题与代表案例

- **#8815：GPU 分类仍受选测错误影响。** 默认和 minimal 的最终 JSON 都明确 `gpu_required`，但推荐测试正文因 context budget 未提供，目标校验抛出 `AI target has no inspected executable test candidate in the merged tree`；有效 GPU 结论随之变成 unknown。正式路径因已有内部回复而通过，但诊断失败不可被绿色结果掩盖。详见证据 zip 中 8815 的 call-4/call-6 response 与 request。未修改 #10020。
- **#8081 / #8433：历史源树与当前 CI 路径不一致。** 两次都请求历史树中不存在的 `scripts/infra/task_jit_run_tests_part*.sh` 等路径，校验拒绝并最终 unknown。相应历史树保留的是旧路径，不能称为原 PR 当时的 bot 生产故障。
- **#9693：缺少可选 case 不代表 CPU-only。** minimal 后保留 `gpu_required`、targets 为空，并指出 persistent decode barrier / empty-KV 的 GPU 同步影响。符合独立判断要求。
- **#3827：docs 标题包含运行时改动。** diff 除文档还增加 GegluTanh 的 enum/helper 分支；无内部回复，模型判 GPU 并失败。但固定历史源树尚未确认该 helper 的 GPU 消费路径，不能用当前版本调用方替代历史证据，因此人工结论保留待确认。
- **#8889：Python 文件也可纯文档。** 实际只改 DeepGEMM docstrings/doctest 文本，正确豁免。
- **#8561：experimental 豁免不是 CPU-only。** 实际修改 GPU top-k radix/barrier 和 GPU 测试，但改动完全受 experimental 路径包含策略豁免。
- **#8932：重试恢复。** 默认阶段文件请求失败，minimal 后按 lazy import/打包元数据的 CPU 行为正确放行。
- **#5658：分类接口的标签局限。** 实际是 experimental SM110 CUDA kernel 改动，另有 benchmark shape JSON；模型以 experimental 豁免为理由输出 cpu_only。当前模型枚举只有 docs_only/cpu_only/gpu_required/unknown，experimental_only 仅为路径快捷分支的输出，因此这属于标签表达局限，不是模型选择了非法类别，也不是错误放行。按行为语义计 1 个分类标签不符，不计为正式误放行。

- **#6458：公开回复不能替代内部回复。** 原始快照中有公开 bot 回复，但没有符合内部规则的回复；正式检查为 waiting_for_bot/failure。
- **#9706 / #9669 / #9550：通用文件名兜底被实际使用。** 输出保留 filename_only_evidence，分别涉及预算省略的 CUDA/JIT 或 GPU Python 文件；没有为文件添加特例。另有 12 例缺少部分原始 patch，分析仍使用可用内容，没有统一否决。
- **#1163 / #8081：新增测试同样纳入 GPU 判断。** 前者新增 CUDA green context API 和设备测试，无内部回复而正式失败；后者即使新增的 PTX 检查可在 CPU 执行，实际同步代码仍被纳入审阅。

## 完整结果表

“分类”在有内部回复的样本中来自另做的无回复诊断；正式检查仅依原始评论计算。Exp=experimental-only。详情 JSON 包含全部 SHA、评论链接、错误、重试和人工判断理由。

| # | 原 PR | 实验 PR | 状态详情 | 分类 | 内部回复 | 正式 | minimal | 人工对照 |
|---|---|---|---|---|---|---|---|---|
| 1 | [#9369](https://github.com/flashinfer-ai/flashinfer/pull/9369) | [#176](https://github.com/kangbintNV/flashinfer/pull/176) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9369.json) | 文档 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9369#issuecomment-6806129216) | ✅ | 无 | 正确放行 |
| 2 | [#9045](https://github.com/flashinfer-ai/flashinfer/pull/9045) | [#177](https://github.com/kangbintNV/flashinfer/pull/177) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9045.json) | 文档 | 无 | ✅ | 无 | 正确放行 |
| 3 | [#7135](https://github.com/flashinfer-ai/flashinfer/pull/7135) | [#178](https://github.com/kangbintNV/flashinfer/pull/178) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/7135.json) | 文档 | 无 | ✅ | 无 | 正确放行 |
| 4 | [#6412](https://github.com/flashinfer-ai/flashinfer/pull/6412) | [#180](https://github.com/kangbintNV/flashinfer/pull/180) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/6412.json) | 文档 | 无 | ✅ | 无 | 正确放行 |
| 5 | [#4162](https://github.com/flashinfer-ai/flashinfer/pull/4162) | [#179](https://github.com/kangbintNV/flashinfer/pull/179) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/4162.json) | 文档 | 无 | ✅ | 无 | 正确放行 |
| 6 | [#3941](https://github.com/flashinfer-ai/flashinfer/pull/3941) | [#181](https://github.com/kangbintNV/flashinfer/pull/181) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/3941.json) | 文档 | 无 | ✅ | 无 | 正确放行 |
| 7 | [#9639](https://github.com/flashinfer-ai/flashinfer/pull/9639) | [#182](https://github.com/kangbintNV/flashinfer/pull/182) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9639.json) | CPU | 无 | ✅ | 无 | 正确放行 |
| 8 | [#9655](https://github.com/flashinfer-ai/flashinfer/pull/9655) | [#183](https://github.com/kangbintNV/flashinfer/pull/183) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9655.json) | CPU | 无 | ✅ | 无 | 正确放行 |
| 9 | [#9739](https://github.com/flashinfer-ai/flashinfer/pull/9739) | [#184](https://github.com/kangbintNV/flashinfer/pull/184) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9739.json) | CPU | [有](https://github.com/flashinfer-ai/flashinfer/pull/9739#issuecomment-7026412299) | ✅ | 无 | 正确放行 |
| 10 | [#4945](https://github.com/flashinfer-ai/flashinfer/pull/4945) | [#185](https://github.com/kangbintNV/flashinfer/pull/185) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/4945.json) | CPU | 无 | ✅ | 无 | 正确放行 |
| 11 | [#5383](https://github.com/flashinfer-ai/flashinfer/pull/5383) | [#186](https://github.com/kangbintNV/flashinfer/pull/186) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/5383.json) | 文档 | 无 | ✅ | 无 | 正确放行 |
| 12 | [#9465](https://github.com/flashinfer-ai/flashinfer/pull/9465) | [#187](https://github.com/kangbintNV/flashinfer/pull/187) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9465.json) | CPU | 无 | ✅ | 无 | 正确放行 |
| 13 | [#7077](https://github.com/flashinfer-ai/flashinfer/pull/7077) | [#188](https://github.com/kangbintNV/flashinfer/pull/188) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/7077.json) | Exp 豁免 | 无 | ✅ | 无 | 正确放行 |
| 14 | [#8561](https://github.com/flashinfer-ai/flashinfer/pull/8561) | [#189](https://github.com/kangbintNV/flashinfer/pull/189) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/8561.json) | Exp 豁免 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8561#issuecomment-6615835702) | ✅ | 无 | 正确放行 |
| 15 | [#9200](https://github.com/flashinfer-ai/flashinfer/pull/9200) | [#190](https://github.com/kangbintNV/flashinfer/pull/190) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9200.json) | Exp 豁免 | 无 | ✅ | 无 | 正确放行 |
| 16 | [#7653](https://github.com/flashinfer-ai/flashinfer/pull/7653) | [#191](https://github.com/kangbintNV/flashinfer/pull/191) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/7653.json) | Exp 豁免 | 无 | ✅ | 无 | 正确放行 |
| 17 | [#9681](https://github.com/flashinfer-ai/flashinfer/pull/9681) | [#192](https://github.com/kangbintNV/flashinfer/pull/192) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9681.json) | GPU | 无 | ❌ | 无 | 待确认 |
| 18 | [#9481](https://github.com/flashinfer-ai/flashinfer/pull/9481) | [#193](https://github.com/kangbintNV/flashinfer/pull/193) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9481.json) | GPU | [有](https://github.com/flashinfer-ai/flashinfer/pull/9481#issuecomment-6905229082) | ✅ | 无 | 正确放行 |
| 19 | [#9738](https://github.com/flashinfer-ai/flashinfer/pull/9738) | [#194](https://github.com/kangbintNV/flashinfer/pull/194) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9738.json) | GPU | [有](https://github.com/flashinfer-ai/flashinfer/pull/9738#issuecomment-7024609809) | ✅ | 无 | 正确放行 |
| 20 | [#9395](https://github.com/flashinfer-ai/flashinfer/pull/9395) | [#195](https://github.com/kangbintNV/flashinfer/pull/195) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9395.json) | GPU | [有](https://github.com/flashinfer-ai/flashinfer/pull/9395#issuecomment-7034539081) | ✅ | 无 | 正确放行 |
| 21 | [#9706](https://github.com/flashinfer-ai/flashinfer/pull/9706) | [#196](https://github.com/kangbintNV/flashinfer/pull/196) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9706.json) | GPU | 无 | ❌ | 无 | 正确判阻塞 |
| 22 | [#9669](https://github.com/flashinfer-ai/flashinfer/pull/9669) | [#197](https://github.com/kangbintNV/flashinfer/pull/197) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9669.json) | GPU | 无 | ❌ | 无 | 正确判阻塞 |
| 23 | [#9375](https://github.com/flashinfer-ai/flashinfer/pull/9375) | [#198](https://github.com/kangbintNV/flashinfer/pull/198) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9375.json) | GPU | 无 | ❌ | 无 | 正确判阻塞 |
| 24 | [#10036](https://github.com/flashinfer-ai/flashinfer/pull/10036) | [#199](https://github.com/kangbintNV/flashinfer/pull/199) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/10036.json) | GPU | 无 | ❌ | 无 | 正确判阻塞 |
| 25 | [#9659](https://github.com/flashinfer-ai/flashinfer/pull/9659) | [#200](https://github.com/kangbintNV/flashinfer/pull/200) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9659.json) | GPU | 无 | ❌ | 无 | 正确判阻塞 |
| 26 | [#9649](https://github.com/flashinfer-ai/flashinfer/pull/9649) | [#201](https://github.com/kangbintNV/flashinfer/pull/201) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9649.json) | GPU | [有](https://github.com/flashinfer-ai/flashinfer/pull/9649#issuecomment-6971883491) | ✅ | 无 | 正确放行 |
| 27 | [#9949](https://github.com/flashinfer-ai/flashinfer/pull/9949) | [#202](https://github.com/kangbintNV/flashinfer/pull/202) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9949.json) | GPU | [有](https://github.com/flashinfer-ai/flashinfer/pull/9949#issuecomment-7121771998) | ✅ | 无 | 正确放行 |
| 28 | [#9550](https://github.com/flashinfer-ai/flashinfer/pull/9550) | [#203](https://github.com/kangbintNV/flashinfer/pull/203) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9550.json) | GPU | 无 | ❌ | 无 | 正确判阻塞 |
| 29 | [#5658](https://github.com/flashinfer-ai/flashinfer/pull/5658) | [#204](https://github.com/kangbintNV/flashinfer/pull/204) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/5658.json) | CPU | [有](https://github.com/flashinfer-ai/flashinfer/pull/5658#issuecomment-5880412590) | ✅ | 无 | 正确放行 |
| 30 | [#8081](https://github.com/flashinfer-ai/flashinfer/pull/8081) | [#205](https://github.com/kangbintNV/flashinfer/pull/205) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/8081.json) | unknown | [有](https://github.com/flashinfer-ai/flashinfer/pull/8081#issuecomment-6863992253) | ✅ | 仍失败 | 正确放行 |
| 31 | [#6711](https://github.com/flashinfer-ai/flashinfer/pull/6711) | [#206](https://github.com/kangbintNV/flashinfer/pull/206) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/6711.json) | GPU | [有](https://github.com/flashinfer-ai/flashinfer/pull/6711#issuecomment-6974039523) | ✅ | 无 | 正确放行 |
| 32 | [#9554](https://github.com/flashinfer-ai/flashinfer/pull/9554) | [#207](https://github.com/kangbintNV/flashinfer/pull/207) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9554.json) | GPU | [有](https://github.com/flashinfer-ai/flashinfer/pull/9554#issuecomment-7076077410) | ✅ | 无 | 正确放行 |
| 33 | [#8766](https://github.com/flashinfer-ai/flashinfer/pull/8766) | [#208](https://github.com/kangbintNV/flashinfer/pull/208) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/8766.json) | GPU | [有](https://github.com/flashinfer-ai/flashinfer/pull/8766#issuecomment-6806546114) | ✅ | 无 | 正确放行 |
| 34 | [#6160](https://github.com/flashinfer-ai/flashinfer/pull/6160) | [#209](https://github.com/kangbintNV/flashinfer/pull/209) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/6160.json) | GPU | [有](https://github.com/flashinfer-ai/flashinfer/pull/6160#issuecomment-6512300092) | ✅ | 无 | 正确放行 |
| 35 | [#9327](https://github.com/flashinfer-ai/flashinfer/pull/9327) | [#210](https://github.com/kangbintNV/flashinfer/pull/210) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9327.json) | GPU | [有](https://github.com/flashinfer-ai/flashinfer/pull/9327#issuecomment-6782877152) | ✅ | 无 | 正确放行 |
| 36 | [#9289](https://github.com/flashinfer-ai/flashinfer/pull/9289) | [#211](https://github.com/kangbintNV/flashinfer/pull/211) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9289.json) | GPU | [有](https://github.com/flashinfer-ai/flashinfer/pull/9289#issuecomment-6983472392) | ✅ | 无 | 正确放行 |
| 37 | [#1163](https://github.com/flashinfer-ai/flashinfer/pull/1163) | [#212](https://github.com/kangbintNV/flashinfer/pull/212) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/1163.json) | GPU | 无 | ❌ | 无 | 正确判阻塞 |
| 38 | [#9478](https://github.com/flashinfer-ai/flashinfer/pull/9478) | [#213](https://github.com/kangbintNV/flashinfer/pull/213) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9478.json) | CPU | [有](https://github.com/flashinfer-ai/flashinfer/pull/9478#issuecomment-6905221665) | ✅ | 无 | 正确放行 |
| 39 | [#8889](https://github.com/flashinfer-ai/flashinfer/pull/8889) | [#214](https://github.com/kangbintNV/flashinfer/pull/214) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/8889.json) | 文档 | 无 | ✅ | 无 | 正确放行 |
| 40 | [#9765](https://github.com/flashinfer-ai/flashinfer/pull/9765) | [#215](https://github.com/kangbintNV/flashinfer/pull/215) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9765.json) | GPU | [有](https://github.com/flashinfer-ai/flashinfer/pull/9765#issuecomment-7034104120) | ✅ | 无 | 正确放行 |
| 41 | [#9693](https://github.com/flashinfer-ai/flashinfer/pull/9693) | [#216](https://github.com/kangbintNV/flashinfer/pull/216) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9693.json) | GPU | [有](https://github.com/flashinfer-ai/flashinfer/pull/9693#issuecomment-7001872107) | ✅ | 恢复 | 正确放行 |
| 42 | [#9687](https://github.com/flashinfer-ai/flashinfer/pull/9687) | [#217](https://github.com/kangbintNV/flashinfer/pull/217) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9687.json) | GPU | [有](https://github.com/flashinfer-ai/flashinfer/pull/9687#issuecomment-7010123047) | ✅ | 无 | 正确放行 |
| 43 | [#8815](https://github.com/flashinfer-ai/flashinfer/pull/8815) | [#218](https://github.com/kangbintNV/flashinfer/pull/218) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/8815.json) | unknown | [有](https://github.com/flashinfer-ai/flashinfer/pull/8815#issuecomment-6667722519) | ✅ | 仍失败 | 正确放行 |
| 44 | [#6458](https://github.com/flashinfer-ai/flashinfer/pull/6458) | [#219](https://github.com/kangbintNV/flashinfer/pull/219) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/6458.json) | GPU | 无 | ❌ | 无 | 正确判阻塞 |
| 45 | [#9640](https://github.com/flashinfer-ai/flashinfer/pull/9640) | [#220](https://github.com/kangbintNV/flashinfer/pull/220) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/9640.json) | GPU | [有](https://github.com/flashinfer-ai/flashinfer/pull/9640#issuecomment-6969555053) | ✅ | 无 | 正确放行 |
| 46 | [#8433](https://github.com/flashinfer-ai/flashinfer/pull/8433) | [#221](https://github.com/kangbintNV/flashinfer/pull/221) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/8433.json) | unknown | [有](https://github.com/flashinfer-ai/flashinfer/pull/8433#issuecomment-6619666965) | ✅ | 仍失败 | 正确放行 |
| 47 | [#7067](https://github.com/flashinfer-ai/flashinfer/pull/7067) | [#222](https://github.com/kangbintNV/flashinfer/pull/222) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/7067.json) | GPU | 无 | ❌ | 无 | 待确认 |
| 48 | [#8932](https://github.com/flashinfer-ai/flashinfer/pull/8932) | [#223](https://github.com/kangbintNV/flashinfer/pull/223) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/8932.json) | CPU | 无 | ✅ | 恢复 | 正确放行 |
| 49 | [#7819](https://github.com/flashinfer-ai/flashinfer/pull/7819) | [#224](https://github.com/kangbintNV/flashinfer/pull/224) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/7819.json) | GPU | 无 | ❌ | 无 | 正确判阻塞 |
| 50 | [#3827](https://github.com/flashinfer-ai/flashinfer/pull/3827) | [#225](https://github.com/kangbintNV/flashinfer/pull/225) | [详情](https://github.com/kangbintNV/flashinfer/blob/codex/bot-run-fresh50-20261126/results/results/3827.json) | GPU | 无 | ❌ | 无 | 待确认 |

## 验证范围与不能证明的部分

已覆盖：固定代码真实入口、冻结源 diff/评论、回复快捷通过、公开 bot 回复排除、文档/CPU/experimental 豁免、无可选 case 时的 GPU 判断、一次 minimal 重试及未知结果保守处理。GPU 与 case 完全独立的要求仍受 #8815 所示错误耦合影响，不能视为全部通过。CPU 验证 44 项通过。
不能证明：GPU 数值/性能正确、测试覆盖充分、真实 bot 服务健康、最新 commit 已实际测试、Actions 事件自动触发、原生 Check Run 发布，以及 Required check 是否真的禁止合并。本批没有 GPU 测试，也没有发送 /bot run 命令。
表中的人工对照来自本次助手逐例静态审阅，并非独立维护者标注；仅判断改动类别及策略合理性，不是对全部 kernel 实现的完整代码审查。无法独立确认的边界保留待确认；模型为非确定输出，本结果不应当作跨版本因果 A/B。

## 数据

[最终 GitHub 状态核对](final-verification.json) · [问题复现索引](issues.json) · [CSV](results.csv) · [完整 JSON](results.json) · [人工审阅](manual-audit.json) · [源/评论审计](remote-audit.json) · [排重集合](exclusions.json) · [请求响应证据包](evidence-traces.zip)
