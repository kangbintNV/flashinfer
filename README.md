# Bot Run Request Check：移除 experimental 豁免后的 150 PR 实验

固定检查器：[b53d126acf2ca62abff733af5525ebd522035750](https://github.com/flashinfer-ai/flashinfer/commit/b53d126acf2ca62abff733af5525ebd522035750)，PR #10020。

## 当前状态

原 100 个实验 PR 已更新，另建 50 个新实验 PR。已核对原始 diff/源码树、评论快照和全部 750 个检查器文件版本。当前已验证的原生正式 Check 数：**0/150**。
如果显示“未运行”，表示尚未获得实际 Actions 执行结果，不能读作 unknown、通过或失败。fork 的 Actions dispatch 曾返回 disabled；没有将 commit status 充作原生 Check Run。已准备的手动工作流只运行检查器，不运行 GPU 测试。

## 修正规则与验证

- 删除 experimental 目录快捷放行、模型 prompt 豁免和旧 experimental-only 分类缓存。GPU 改动无论是否 experimental，都需要有效内部回复；docs/CPU 仍按实际行为豁免。
- 历史内部回复仍有效，不要求 pipeline 启动/通过；公开 bot 回复不替代内部回复。原始回复缺席时才分析代码，失败/unknown 以 minimal 重试一次。
- 回归测试先复现 5 个失败断言；修正后 47 项 gate、66 项 infra 和 10 项 transport 测试通过，changed-file pre-commit 通过。
- 本地实时 #5658 预检已由 cpu_only 改为 gpu_required；它不是原生正式实验结果，不计入结果总数。
- 原 100 个样本和新增 50 个原 PR 无重复，另排除了保守排重清单中的其他历史原 PR。候选 #4903 因落地 diff 为空在推理前剔除，以 #2541 替换。
- 旧 50 中 8 个 PR 的原分支 head blob 与落地 merged blob 不同；21 个文件的净增删行均一致，原始冻结 files/comments 也完全保留。此为原有 merge-context 差异，本次未改写成一致；详见 legacy-blob-audit.json。所有 150 个源前后树及净改动均已核对。
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
    "not_run": 150
  },
  "formal_assessment": {
    "not_run": 150
  },
  "classifications": {
    "not_run": 150
  },
  "classification_assessment": {
    "not_run": 150
  },
  "native_formal_checks_verified": 0,
  "minimal_retry_cases": 0,
  "native_infrastructure_failures": 0,
  "source_integrity_verified": 150,
  "legacy_original_head_merged_blob_difference_prs": 8,
  "gpu_tests_started": 0,
  "bot_commands_posted": 0
}
```

## 完整结果表

有内部回复时，“分类”来自独立无回复诊断；它不替代正式结论。正式结果及链接只取实际原生 Check Run。

| 原 PR | 实验 PR | 批次 | 内部回复 | 正式 Check | 分类 | minimal | 助手审阅预期 |
|---|---|---|---|---|---|---|---|
| [#9788](https://github.com/flashinfer-ai/flashinfer/pull/9788) | [#126](https://github.com/kangbintNV/flashinfer/pull/126) | old50 | 无 | 未运行 | 未运行 | — | CPU |
| [#10013](https://github.com/flashinfer-ai/flashinfer/pull/10013) | [#127](https://github.com/kangbintNV/flashinfer/pull/127) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/10013#issuecomment-7152368777) | 未运行 | 未运行 | — | GPU |
| [#9731](https://github.com/flashinfer-ai/flashinfer/pull/9731) | [#128](https://github.com/kangbintNV/flashinfer/pull/128) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9731#issuecomment-7117140767) | 未运行 | 未运行 | — | GPU |
| [#10005](https://github.com/flashinfer-ai/flashinfer/pull/10005) | [#129](https://github.com/kangbintNV/flashinfer/pull/129) | old50 | 无 | 未运行 | 未运行 | — | 审阅未定 |
| [#10006](https://github.com/flashinfer-ai/flashinfer/pull/10006) | [#130](https://github.com/kangbintNV/flashinfer/pull/130) | old50 | 无 | 未运行 | 未运行 | — | 审阅未定 |
| [#9989](https://github.com/flashinfer-ai/flashinfer/pull/9989) | [#131](https://github.com/kangbintNV/flashinfer/pull/131) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9989#issuecomment-7141676310) | 未运行 | 未运行 | — | GPU |
| [#9990](https://github.com/flashinfer-ai/flashinfer/pull/9990) | [#132](https://github.com/kangbintNV/flashinfer/pull/132) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9990#issuecomment-7137423935) | 未运行 | 未运行 | — | CPU |
| [#9916](https://github.com/flashinfer-ai/flashinfer/pull/9916) | [#133](https://github.com/kangbintNV/flashinfer/pull/133) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9916#issuecomment-7119623448) | 未运行 | 未运行 | — | GPU |
| [#9978](https://github.com/flashinfer-ai/flashinfer/pull/9978) | [#134](https://github.com/kangbintNV/flashinfer/pull/134) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9978#issuecomment-7130412330) | 未运行 | 未运行 | — | GPU |
| [#9964](https://github.com/flashinfer-ai/flashinfer/pull/9964) | [#135](https://github.com/kangbintNV/flashinfer/pull/135) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9964#issuecomment-7131410753) | 未运行 | 未运行 | — | GPU |
| [#9958](https://github.com/flashinfer-ai/flashinfer/pull/9958) | [#136](https://github.com/kangbintNV/flashinfer/pull/136) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9958#issuecomment-7122388075) | 未运行 | 未运行 | — | GPU |
| [#9991](https://github.com/flashinfer-ai/flashinfer/pull/9991) | [#137](https://github.com/kangbintNV/flashinfer/pull/137) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9991#issuecomment-7137430127) | 未运行 | 未运行 | — | GPU |
| [#9817](https://github.com/flashinfer-ai/flashinfer/pull/9817) | [#138](https://github.com/kangbintNV/flashinfer/pull/138) | old50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9716](https://github.com/flashinfer-ai/flashinfer/pull/9716) | [#139](https://github.com/kangbintNV/flashinfer/pull/139) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9716#issuecomment-7119967898) | 未运行 | 未运行 | — | GPU |
| [#9974](https://github.com/flashinfer-ai/flashinfer/pull/9974) | [#140](https://github.com/kangbintNV/flashinfer/pull/140) | old50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9892](https://github.com/flashinfer-ai/flashinfer/pull/9892) | [#141](https://github.com/kangbintNV/flashinfer/pull/141) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9892#issuecomment-7131921554) | 未运行 | 未运行 | — | GPU |
| [#9885](https://github.com/flashinfer-ai/flashinfer/pull/9885) | [#142](https://github.com/kangbintNV/flashinfer/pull/142) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9885#issuecomment-7122274355) | 未运行 | 未运行 | — | GPU |
| [#9651](https://github.com/flashinfer-ai/flashinfer/pull/9651) | [#143](https://github.com/kangbintNV/flashinfer/pull/143) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9651#issuecomment-7120452466) | 未运行 | 未运行 | — | GPU |
| [#9876](https://github.com/flashinfer-ai/flashinfer/pull/9876) | [#144](https://github.com/kangbintNV/flashinfer/pull/144) | old50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9917](https://github.com/flashinfer-ai/flashinfer/pull/9917) | [#145](https://github.com/kangbintNV/flashinfer/pull/145) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9917#issuecomment-7118627807) | 未运行 | 未运行 | — | GPU |
| [#9816](https://github.com/flashinfer-ai/flashinfer/pull/9816) | [#146](https://github.com/kangbintNV/flashinfer/pull/146) | old50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9815](https://github.com/flashinfer-ai/flashinfer/pull/9815) | [#147](https://github.com/kangbintNV/flashinfer/pull/147) | old50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9814](https://github.com/flashinfer-ai/flashinfer/pull/9814) | [#148](https://github.com/kangbintNV/flashinfer/pull/148) | old50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9813](https://github.com/flashinfer-ai/flashinfer/pull/9813) | [#149](https://github.com/kangbintNV/flashinfer/pull/149) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9813#issuecomment-7073352142) | 未运行 | 未运行 | — | GPU |
| [#9771](https://github.com/flashinfer-ai/flashinfer/pull/9771) | [#150](https://github.com/kangbintNV/flashinfer/pull/150) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9771#issuecomment-7093273577) | 未运行 | 未运行 | — | GPU |
| [#9819](https://github.com/flashinfer-ai/flashinfer/pull/9819) | [#151](https://github.com/kangbintNV/flashinfer/pull/151) | old50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9908](https://github.com/flashinfer-ai/flashinfer/pull/9908) | [#152](https://github.com/kangbintNV/flashinfer/pull/152) | old50 | 无 | 未运行 | 未运行 | — | CPU |
| [#9897](https://github.com/flashinfer-ai/flashinfer/pull/9897) | [#153](https://github.com/kangbintNV/flashinfer/pull/153) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9897#issuecomment-7115181575) | 未运行 | 未运行 | — | GPU |
| [#9844](https://github.com/flashinfer-ai/flashinfer/pull/9844) | [#154](https://github.com/kangbintNV/flashinfer/pull/154) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9844#issuecomment-7076553375) | 未运行 | 未运行 | — | GPU |
| [#9843](https://github.com/flashinfer-ai/flashinfer/pull/9843) | [#155](https://github.com/kangbintNV/flashinfer/pull/155) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9843#issuecomment-7076551897) | 未运行 | 未运行 | — | 审阅未定 |
| [#9694](https://github.com/flashinfer-ai/flashinfer/pull/9694) | [#156](https://github.com/kangbintNV/flashinfer/pull/156) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9694#issuecomment-7035450417) | 未运行 | 未运行 | — | GPU |
| [#9847](https://github.com/flashinfer-ai/flashinfer/pull/9847) | [#157](https://github.com/kangbintNV/flashinfer/pull/157) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9847#issuecomment-7077462090) | 未运行 | 未运行 | — | CPU |
| [#9861](https://github.com/flashinfer-ai/flashinfer/pull/9861) | [#158](https://github.com/kangbintNV/flashinfer/pull/158) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9861#issuecomment-7094014552) | 未运行 | 未运行 | — | GPU |
| [#9871](https://github.com/flashinfer-ai/flashinfer/pull/9871) | [#159](https://github.com/kangbintNV/flashinfer/pull/159) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9871#issuecomment-7102324850) | 未运行 | 未运行 | — | GPU |
| [#9865](https://github.com/flashinfer-ai/flashinfer/pull/9865) | [#160](https://github.com/kangbintNV/flashinfer/pull/160) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9865#issuecomment-7093929737) | 未运行 | 未运行 | — | GPU |
| [#9894](https://github.com/flashinfer-ai/flashinfer/pull/9894) | [#161](https://github.com/kangbintNV/flashinfer/pull/161) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9894#issuecomment-7106000551) | 未运行 | 未运行 | — | CPU |
| [#9836](https://github.com/flashinfer-ai/flashinfer/pull/9836) | [#162](https://github.com/kangbintNV/flashinfer/pull/162) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9836#issuecomment-7091022464) | 未运行 | 未运行 | — | GPU |
| [#9846](https://github.com/flashinfer-ai/flashinfer/pull/9846) | [#163](https://github.com/kangbintNV/flashinfer/pull/163) | old50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9749](https://github.com/flashinfer-ai/flashinfer/pull/9749) | [#164](https://github.com/kangbintNV/flashinfer/pull/164) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9749#issuecomment-7028226027) | 未运行 | 未运行 | — | GPU |
| [#9858](https://github.com/flashinfer-ai/flashinfer/pull/9858) | [#165](https://github.com/kangbintNV/flashinfer/pull/165) | old50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9857](https://github.com/flashinfer-ai/flashinfer/pull/9857) | [#166](https://github.com/kangbintNV/flashinfer/pull/166) | old50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9834](https://github.com/flashinfer-ai/flashinfer/pull/9834) | [#167](https://github.com/kangbintNV/flashinfer/pull/167) | old50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9818](https://github.com/flashinfer-ai/flashinfer/pull/9818) | [#168](https://github.com/kangbintNV/flashinfer/pull/168) | old50 | 无 | 未运行 | 未运行 | — | CPU |
| [#9358](https://github.com/flashinfer-ai/flashinfer/pull/9358) | [#169](https://github.com/kangbintNV/flashinfer/pull/169) | old50 | 无 | 未运行 | 未运行 | — | 文档 |
| [#9332](https://github.com/flashinfer-ai/flashinfer/pull/9332) | [#170](https://github.com/kangbintNV/flashinfer/pull/170) | old50 | 无 | 未运行 | 未运行 | — | CPU |
| [#9307](https://github.com/flashinfer-ai/flashinfer/pull/9307) | [#171](https://github.com/kangbintNV/flashinfer/pull/171) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9307#issuecomment-6785807973) | 未运行 | 未运行 | — | CPU |
| [#9545](https://github.com/flashinfer-ai/flashinfer/pull/9545) | [#172](https://github.com/kangbintNV/flashinfer/pull/172) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9545#issuecomment-6957693037) | 未运行 | 未运行 | — | 文档 |
| [#8464](https://github.com/flashinfer-ai/flashinfer/pull/8464) | [#173](https://github.com/kangbintNV/flashinfer/pull/173) | old50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8464#issuecomment-6659423942) | 未运行 | 未运行 | — | 文档 |
| [#8960](https://github.com/flashinfer-ai/flashinfer/pull/8960) | [#174](https://github.com/kangbintNV/flashinfer/pull/174) | old50 | 无 | 未运行 | 未运行 | — | 文档 |
| [#8930](https://github.com/flashinfer-ai/flashinfer/pull/8930) | [#175](https://github.com/kangbintNV/flashinfer/pull/175) | old50 | 无 | 未运行 | 未运行 | — | 文档 |
| [#9369](https://github.com/flashinfer-ai/flashinfer/pull/9369) | [#176](https://github.com/kangbintNV/flashinfer/pull/176) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9369#issuecomment-6806129216) | 未运行 | 未运行 | — | 文档 |
| [#9045](https://github.com/flashinfer-ai/flashinfer/pull/9045) | [#177](https://github.com/kangbintNV/flashinfer/pull/177) | fresh50 | 无 | 未运行 | 未运行 | — | 文档 |
| [#7135](https://github.com/flashinfer-ai/flashinfer/pull/7135) | [#178](https://github.com/kangbintNV/flashinfer/pull/178) | fresh50 | 无 | 未运行 | 未运行 | — | 文档 |
| [#4162](https://github.com/flashinfer-ai/flashinfer/pull/4162) | [#179](https://github.com/kangbintNV/flashinfer/pull/179) | fresh50 | 无 | 未运行 | 未运行 | — | 文档 |
| [#6412](https://github.com/flashinfer-ai/flashinfer/pull/6412) | [#180](https://github.com/kangbintNV/flashinfer/pull/180) | fresh50 | 无 | 未运行 | 未运行 | — | 文档 |
| [#3941](https://github.com/flashinfer-ai/flashinfer/pull/3941) | [#181](https://github.com/kangbintNV/flashinfer/pull/181) | fresh50 | 无 | 未运行 | 未运行 | — | 文档 |
| [#9639](https://github.com/flashinfer-ai/flashinfer/pull/9639) | [#182](https://github.com/kangbintNV/flashinfer/pull/182) | fresh50 | 无 | 未运行 | 未运行 | — | CPU |
| [#9655](https://github.com/flashinfer-ai/flashinfer/pull/9655) | [#183](https://github.com/kangbintNV/flashinfer/pull/183) | fresh50 | 无 | 未运行 | 未运行 | — | CPU |
| [#9739](https://github.com/flashinfer-ai/flashinfer/pull/9739) | [#184](https://github.com/kangbintNV/flashinfer/pull/184) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9739#issuecomment-7026412299) | 未运行 | 未运行 | — | CPU |
| [#4945](https://github.com/flashinfer-ai/flashinfer/pull/4945) | [#185](https://github.com/kangbintNV/flashinfer/pull/185) | fresh50 | 无 | 未运行 | 未运行 | — | CPU |
| [#5383](https://github.com/flashinfer-ai/flashinfer/pull/5383) | [#186](https://github.com/kangbintNV/flashinfer/pull/186) | fresh50 | 无 | 未运行 | 未运行 | — | CPU |
| [#9465](https://github.com/flashinfer-ai/flashinfer/pull/9465) | [#187](https://github.com/kangbintNV/flashinfer/pull/187) | fresh50 | 无 | 未运行 | 未运行 | — | CPU |
| [#7077](https://github.com/flashinfer-ai/flashinfer/pull/7077) | [#188](https://github.com/kangbintNV/flashinfer/pull/188) | fresh50 | 无 | 未运行 | 未运行 | — | CPU |
| [#8561](https://github.com/flashinfer-ai/flashinfer/pull/8561) | [#189](https://github.com/kangbintNV/flashinfer/pull/189) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8561#issuecomment-6661899364) | 未运行 | 未运行 | — | GPU |
| [#9200](https://github.com/flashinfer-ai/flashinfer/pull/9200) | [#190](https://github.com/kangbintNV/flashinfer/pull/190) | fresh50 | 无 | 未运行 | 未运行 | — | 文档 |
| [#7653](https://github.com/flashinfer-ai/flashinfer/pull/7653) | [#191](https://github.com/kangbintNV/flashinfer/pull/191) | fresh50 | 无 | 未运行 | 未运行 | — | 文档 |
| [#9681](https://github.com/flashinfer-ai/flashinfer/pull/9681) | [#192](https://github.com/kangbintNV/flashinfer/pull/192) | fresh50 | 无 | 未运行 | 未运行 | — | 审阅未定 |
| [#9481](https://github.com/flashinfer-ai/flashinfer/pull/9481) | [#193](https://github.com/kangbintNV/flashinfer/pull/193) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9481#issuecomment-6905895364) | 未运行 | 未运行 | — | 审阅未定 |
| [#9738](https://github.com/flashinfer-ai/flashinfer/pull/9738) | [#194](https://github.com/kangbintNV/flashinfer/pull/194) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9738#issuecomment-7025271294) | 未运行 | 未运行 | — | GPU |
| [#9395](https://github.com/flashinfer-ai/flashinfer/pull/9395) | [#195](https://github.com/kangbintNV/flashinfer/pull/195) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9395#issuecomment-7132488096) | 未运行 | 未运行 | — | GPU |
| [#9706](https://github.com/flashinfer-ai/flashinfer/pull/9706) | [#196](https://github.com/kangbintNV/flashinfer/pull/196) | fresh50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9669](https://github.com/flashinfer-ai/flashinfer/pull/9669) | [#197](https://github.com/kangbintNV/flashinfer/pull/197) | fresh50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9375](https://github.com/flashinfer-ai/flashinfer/pull/9375) | [#198](https://github.com/kangbintNV/flashinfer/pull/198) | fresh50 | 无 | 未运行 | 未运行 | — | GPU |
| [#10036](https://github.com/flashinfer-ai/flashinfer/pull/10036) | [#199](https://github.com/kangbintNV/flashinfer/pull/199) | fresh50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9659](https://github.com/flashinfer-ai/flashinfer/pull/9659) | [#200](https://github.com/kangbintNV/flashinfer/pull/200) | fresh50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9649](https://github.com/flashinfer-ai/flashinfer/pull/9649) | [#201](https://github.com/kangbintNV/flashinfer/pull/201) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9649#issuecomment-7029324566) | 未运行 | 未运行 | — | GPU |
| [#9949](https://github.com/flashinfer-ai/flashinfer/pull/9949) | [#202](https://github.com/kangbintNV/flashinfer/pull/202) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9949#issuecomment-7181797949) | 未运行 | 未运行 | — | GPU |
| [#9550](https://github.com/flashinfer-ai/flashinfer/pull/9550) | [#203](https://github.com/kangbintNV/flashinfer/pull/203) | fresh50 | 无 | 未运行 | 未运行 | — | GPU |
| [#5658](https://github.com/flashinfer-ai/flashinfer/pull/5658) | [#204](https://github.com/kangbintNV/flashinfer/pull/204) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/5658#issuecomment-5880412590) | 未运行 | 未运行 | — | GPU |
| [#8081](https://github.com/flashinfer-ai/flashinfer/pull/8081) | [#205](https://github.com/kangbintNV/flashinfer/pull/205) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8081#issuecomment-6880608414) | 未运行 | 未运行 | — | GPU |
| [#6711](https://github.com/flashinfer-ai/flashinfer/pull/6711) | [#206](https://github.com/kangbintNV/flashinfer/pull/206) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/6711#issuecomment-6974039523) | 未运行 | 未运行 | — | GPU |
| [#9554](https://github.com/flashinfer-ai/flashinfer/pull/9554) | [#207](https://github.com/kangbintNV/flashinfer/pull/207) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9554#issuecomment-7076077410) | 未运行 | 未运行 | — | GPU |
| [#8766](https://github.com/flashinfer-ai/flashinfer/pull/8766) | [#208](https://github.com/kangbintNV/flashinfer/pull/208) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8766#issuecomment-6983034862) | 未运行 | 未运行 | — | GPU |
| [#6160](https://github.com/flashinfer-ai/flashinfer/pull/6160) | [#209](https://github.com/kangbintNV/flashinfer/pull/209) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/6160#issuecomment-7031181649) | 未运行 | 未运行 | — | GPU |
| [#9327](https://github.com/flashinfer-ai/flashinfer/pull/9327) | [#210](https://github.com/kangbintNV/flashinfer/pull/210) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9327#issuecomment-6783825712) | 未运行 | 未运行 | — | 审阅未定 |
| [#9289](https://github.com/flashinfer-ai/flashinfer/pull/9289) | [#211](https://github.com/kangbintNV/flashinfer/pull/211) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9289#issuecomment-7014293371) | 未运行 | 未运行 | — | GPU |
| [#1163](https://github.com/flashinfer-ai/flashinfer/pull/1163) | [#212](https://github.com/kangbintNV/flashinfer/pull/212) | fresh50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9478](https://github.com/flashinfer-ai/flashinfer/pull/9478) | [#213](https://github.com/kangbintNV/flashinfer/pull/213) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9478#issuecomment-6981486445) | 未运行 | 未运行 | — | CPU |
| [#8889](https://github.com/flashinfer-ai/flashinfer/pull/8889) | [#214](https://github.com/kangbintNV/flashinfer/pull/214) | fresh50 | 无 | 未运行 | 未运行 | — | 文档 |
| [#9765](https://github.com/flashinfer-ai/flashinfer/pull/9765) | [#215](https://github.com/kangbintNV/flashinfer/pull/215) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9765#issuecomment-7034104120) | 未运行 | 未运行 | — | GPU |
| [#9693](https://github.com/flashinfer-ai/flashinfer/pull/9693) | [#216](https://github.com/kangbintNV/flashinfer/pull/216) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9693#issuecomment-7001872107) | 未运行 | 未运行 | — | GPU |
| [#9687](https://github.com/flashinfer-ai/flashinfer/pull/9687) | [#217](https://github.com/kangbintNV/flashinfer/pull/217) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9687#issuecomment-7010123047) | 未运行 | 未运行 | — | GPU |
| [#8815](https://github.com/flashinfer-ai/flashinfer/pull/8815) | [#218](https://github.com/kangbintNV/flashinfer/pull/218) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8815#issuecomment-7020741789) | 未运行 | 未运行 | — | GPU |
| [#6458](https://github.com/flashinfer-ai/flashinfer/pull/6458) | [#219](https://github.com/kangbintNV/flashinfer/pull/219) | fresh50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9640](https://github.com/flashinfer-ai/flashinfer/pull/9640) | [#220](https://github.com/kangbintNV/flashinfer/pull/220) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9640#issuecomment-6969555053) | 未运行 | 未运行 | — | GPU |
| [#8433](https://github.com/flashinfer-ai/flashinfer/pull/8433) | [#221](https://github.com/kangbintNV/flashinfer/pull/221) | fresh50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8433#issuecomment-6624366719) | 未运行 | 未运行 | — | GPU |
| [#7067](https://github.com/flashinfer-ai/flashinfer/pull/7067) | [#222](https://github.com/kangbintNV/flashinfer/pull/222) | fresh50 | 无 | 未运行 | 未运行 | — | 审阅未定 |
| [#8932](https://github.com/flashinfer-ai/flashinfer/pull/8932) | [#223](https://github.com/kangbintNV/flashinfer/pull/223) | fresh50 | 无 | 未运行 | 未运行 | — | CPU |
| [#7819](https://github.com/flashinfer-ai/flashinfer/pull/7819) | [#224](https://github.com/kangbintNV/flashinfer/pull/224) | fresh50 | 无 | 未运行 | 未运行 | — | GPU |
| [#3827](https://github.com/flashinfer-ai/flashinfer/pull/3827) | [#225](https://github.com/kangbintNV/flashinfer/pull/225) | fresh50 | 无 | 未运行 | 未运行 | — | 审阅未定 |
| [#9082](https://github.com/flashinfer-ai/flashinfer/pull/9082) | [#228](https://github.com/kangbintNV/flashinfer/pull/228) | new50 | 无 | 未运行 | 未运行 | — | 文档 |
| [#4948](https://github.com/flashinfer-ai/flashinfer/pull/4948) | [#229](https://github.com/kangbintNV/flashinfer/pull/229) | new50 | 无 | 未运行 | 未运行 | — | 文档 |
| [#8185](https://github.com/flashinfer-ai/flashinfer/pull/8185) | [#230](https://github.com/kangbintNV/flashinfer/pull/230) | new50 | 无 | 未运行 | 未运行 | — | 文档 |
| [#2541](https://github.com/flashinfer-ai/flashinfer/pull/2541) | [#231](https://github.com/kangbintNV/flashinfer/pull/231) | new50 | 无 | 未运行 | 未运行 | — | 文档 |
| [#4175](https://github.com/flashinfer-ai/flashinfer/pull/4175) | [#232](https://github.com/kangbintNV/flashinfer/pull/232) | new50 | 无 | 未运行 | 未运行 | — | 文档 |
| [#3710](https://github.com/flashinfer-ai/flashinfer/pull/3710) | [#233](https://github.com/kangbintNV/flashinfer/pull/233) | new50 | 无 | 未运行 | 未运行 | — | 文档 |
| [#9985](https://github.com/flashinfer-ai/flashinfer/pull/9985) | [#234](https://github.com/kangbintNV/flashinfer/pull/234) | new50 | 无 | 未运行 | 未运行 | — | CPU |
| [#3853](https://github.com/flashinfer-ai/flashinfer/pull/3853) | [#235](https://github.com/kangbintNV/flashinfer/pull/235) | new50 | 无 | 未运行 | 未运行 | — | CPU |
| [#9688](https://github.com/flashinfer-ai/flashinfer/pull/9688) | [#236](https://github.com/kangbintNV/flashinfer/pull/236) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9688#issuecomment-7001181982) | 未运行 | 未运行 | — | CPU |
| [#9462](https://github.com/flashinfer-ai/flashinfer/pull/9462) | [#237](https://github.com/kangbintNV/flashinfer/pull/237) | new50 | 无 | 未运行 | 未运行 | — | 审阅未定 |
| [#7625](https://github.com/flashinfer-ai/flashinfer/pull/7625) | [#238](https://github.com/kangbintNV/flashinfer/pull/238) | new50 | 无 | 未运行 | 未运行 | — | 文档 |
| [#8036](https://github.com/flashinfer-ai/flashinfer/pull/8036) | [#239](https://github.com/kangbintNV/flashinfer/pull/239) | new50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9656](https://github.com/flashinfer-ai/flashinfer/pull/9656) | [#240](https://github.com/kangbintNV/flashinfer/pull/240) | new50 | 无 | 未运行 | 未运行 | — | GPU |
| [#8867](https://github.com/flashinfer-ai/flashinfer/pull/8867) | [#241](https://github.com/kangbintNV/flashinfer/pull/241) | new50 | 无 | 未运行 | 未运行 | — | GPU |
| [#6902](https://github.com/flashinfer-ai/flashinfer/pull/6902) | [#242](https://github.com/kangbintNV/flashinfer/pull/242) | new50 | 无 | 未运行 | 未运行 | — | GPU |
| [#5040](https://github.com/flashinfer-ai/flashinfer/pull/5040) | [#243](https://github.com/kangbintNV/flashinfer/pull/243) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/5040#issuecomment-5610482618) | 未运行 | 未运行 | — | GPU |
| [#8740](https://github.com/flashinfer-ai/flashinfer/pull/8740) | [#245](https://github.com/kangbintNV/flashinfer/pull/245) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8740#issuecomment-6759578978) | 未运行 | 未运行 | — | GPU |
| [#8479](https://github.com/flashinfer-ai/flashinfer/pull/8479) | [#247](https://github.com/kangbintNV/flashinfer/pull/247) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8479#issuecomment-6813765933) | 未运行 | 未运行 | — | GPU |
| [#6790](https://github.com/flashinfer-ai/flashinfer/pull/6790) | [#248](https://github.com/kangbintNV/flashinfer/pull/248) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/6790#issuecomment-6325133828) | 未运行 | 未运行 | — | GPU |
| [#9773](https://github.com/flashinfer-ai/flashinfer/pull/9773) | [#249](https://github.com/kangbintNV/flashinfer/pull/249) | new50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9660](https://github.com/flashinfer-ai/flashinfer/pull/9660) | [#250](https://github.com/kangbintNV/flashinfer/pull/250) | new50 | 无 | 未运行 | 未运行 | — | GPU |
| [#10046](https://github.com/flashinfer-ai/flashinfer/pull/10046) | [#251](https://github.com/kangbintNV/flashinfer/pull/251) | new50 | 无 | 未运行 | 未运行 | — | CPU |
| [#6436](https://github.com/flashinfer-ai/flashinfer/pull/6436) | [#252](https://github.com/kangbintNV/flashinfer/pull/252) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/6436#issuecomment-6760153229) | 未运行 | 未运行 | — | GPU |
| [#5545](https://github.com/flashinfer-ai/flashinfer/pull/5545) | [#253](https://github.com/kangbintNV/flashinfer/pull/253) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/5545#issuecomment-5850911673) | 未运行 | 未运行 | — | GPU |
| [#9112](https://github.com/flashinfer-ai/flashinfer/pull/9112) | [#254](https://github.com/kangbintNV/flashinfer/pull/254) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9112#issuecomment-7169436156) | 未运行 | 未运行 | — | GPU |
| [#9468](https://github.com/flashinfer-ai/flashinfer/pull/9468) | [#255](https://github.com/kangbintNV/flashinfer/pull/255) | new50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9654](https://github.com/flashinfer-ai/flashinfer/pull/9654) | [#256](https://github.com/kangbintNV/flashinfer/pull/256) | new50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9679](https://github.com/flashinfer-ai/flashinfer/pull/9679) | [#257](https://github.com/kangbintNV/flashinfer/pull/257) | new50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9464](https://github.com/flashinfer-ai/flashinfer/pull/9464) | [#258](https://github.com/kangbintNV/flashinfer/pull/258) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9464#issuecomment-6981793114) | 未运行 | 未运行 | — | GPU |
| [#9745](https://github.com/flashinfer-ai/flashinfer/pull/9745) | [#259](https://github.com/kangbintNV/flashinfer/pull/259) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9745#issuecomment-7031186743) | 未运行 | 未运行 | — | GPU |
| [#9379](https://github.com/flashinfer-ai/flashinfer/pull/9379) | [#260](https://github.com/kangbintNV/flashinfer/pull/260) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9379#issuecomment-6842701998) | 未运行 | 未运行 | — | GPU |
| [#8002](https://github.com/flashinfer-ai/flashinfer/pull/8002) | [#261](https://github.com/kangbintNV/flashinfer/pull/261) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8002#issuecomment-6610367880) | 未运行 | 未运行 | — | GPU |
| [#9463](https://github.com/flashinfer-ai/flashinfer/pull/9463) | [#262](https://github.com/kangbintNV/flashinfer/pull/262) | new50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9779](https://github.com/flashinfer-ai/flashinfer/pull/9779) | [#263](https://github.com/kangbintNV/flashinfer/pull/263) | new50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9628](https://github.com/flashinfer-ai/flashinfer/pull/9628) | [#264](https://github.com/kangbintNV/flashinfer/pull/264) | new50 | 无 | 未运行 | 未运行 | — | GPU |
| [#8131](https://github.com/flashinfer-ai/flashinfer/pull/8131) | [#265](https://github.com/kangbintNV/flashinfer/pull/265) | new50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9676](https://github.com/flashinfer-ai/flashinfer/pull/9676) | [#266](https://github.com/kangbintNV/flashinfer/pull/266) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9676#issuecomment-7020916382) | 未运行 | 未运行 | — | GPU |
| [#9329](https://github.com/flashinfer-ai/flashinfer/pull/9329) | [#267](https://github.com/kangbintNV/flashinfer/pull/267) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9329#issuecomment-6881712313) | 未运行 | 未运行 | — | GPU |
| [#9677](https://github.com/flashinfer-ai/flashinfer/pull/9677) | [#268](https://github.com/kangbintNV/flashinfer/pull/268) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9677#issuecomment-7022787743) | 未运行 | 未运行 | — | GPU |
| [#9493](https://github.com/flashinfer-ai/flashinfer/pull/9493) | [#269](https://github.com/kangbintNV/flashinfer/pull/269) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9493#issuecomment-6911100042) | 未运行 | 未运行 | — | GPU |
| [#935](https://github.com/flashinfer-ai/flashinfer/pull/935) | [#270](https://github.com/kangbintNV/flashinfer/pull/270) | new50 | 无 | 未运行 | 未运行 | — | 文档 |
| [#9967](https://github.com/flashinfer-ai/flashinfer/pull/9967) | [#271](https://github.com/kangbintNV/flashinfer/pull/271) | new50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9757](https://github.com/flashinfer-ai/flashinfer/pull/9757) | [#272](https://github.com/kangbintNV/flashinfer/pull/272) | new50 | 无 | 未运行 | 未运行 | — | GPU |
| [#5629](https://github.com/flashinfer-ai/flashinfer/pull/5629) | [#273](https://github.com/kangbintNV/flashinfer/pull/273) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/5629#issuecomment-5865016332) | 未运行 | 未运行 | — | 文档 |
| [#9998](https://github.com/flashinfer-ai/flashinfer/pull/9998) | [#274](https://github.com/kangbintNV/flashinfer/pull/274) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9998#issuecomment-7169964271) | 未运行 | 未运行 | — | GPU |
| [#9848](https://github.com/flashinfer-ai/flashinfer/pull/9848) | [#275](https://github.com/kangbintNV/flashinfer/pull/275) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9848#issuecomment-7144687059) | 未运行 | 未运行 | — | GPU |
| [#9725](https://github.com/flashinfer-ai/flashinfer/pull/9725) | [#276](https://github.com/kangbintNV/flashinfer/pull/276) | new50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9663](https://github.com/flashinfer-ai/flashinfer/pull/9663) | [#277](https://github.com/kangbintNV/flashinfer/pull/277) | new50 | 无 | 未运行 | 未运行 | — | GPU |
| [#9429](https://github.com/flashinfer-ai/flashinfer/pull/9429) | [#278](https://github.com/kangbintNV/flashinfer/pull/278) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/9429#issuecomment-6926082806) | 未运行 | 未运行 | — | GPU |
| [#8549](https://github.com/flashinfer-ai/flashinfer/pull/8549) | [#279](https://github.com/kangbintNV/flashinfer/pull/279) | new50 | [有](https://github.com/flashinfer-ai/flashinfer/pull/8549#issuecomment-6941072903) | 未运行 | 未运行 | — | GPU |

## 能证明与不能证明

最终原生结果完成后可验证固定代码、冻结证据下的门禁判断、分类/重试输出及 GitHub Check 发布。工作流自身成功仅表示实验完成，不代表正式 Bot Run Request Check 通过；GPU 无回复的正式失败是预期结果。
本批不证明 GPU 数值/性能正确、用例覆盖充分、真实 bot 服务健康或当前 commit 实际已测试。未配置 required check/branch protection，不能声称已验证强制合并阻塞。新鲜模型响应非确定，本次不是严格的单变量因果 A/B。
代理没有修改 fork main 或仓库设置；运行中观察到 fork main 被其他活动更新，已另存观察记录，未覆盖或恢复该分支。

## 数据

[CSV](results.csv) · [完整 JSON](results.json) · [助手静态审阅](manual-review.json) · [源码审计](source-audit.json) · [检查器版本](checker-pins.json) · [旧样本 merge-context 差异](legacy-blob-audit.json)
