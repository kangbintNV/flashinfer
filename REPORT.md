# Inference Hub invalid JSON 原因实测

本轮复跑了 7 个历史 invalid JSON 样本和 1 个历史响应不完整对照样本。使用相同固定源码与原始 read_paths 重建最终请求，8/8 上下文序列化长度与原始 Actions 日志一致。模型 azure/anthropic/claude-opus-5，max_tokens=4000；原解析器和原有 temperature 删参重试逻辑保持不变。由于 GitHub 拒绝执行，使用用户指定共享配置中现有文档检查器也使用的 OPENAI_API_KEY 兼容名称，在本地访问同一 NVIDIA Inference Hub 路由。密钥未写入请求文件、日志或报告。

## 结论

- 复跑结果：6 个正常，1 个 Markdown JSON 代码块包装，1 个真正的输出 token 截断。
- #9771：HTTP 200，finish_reason=stop，completion_tokens=3163，响应体17762字节。内容以 ```json 开头、以 ``` 结束；json.loads(content) 在第1列报 Expecting value。去掉完整外层代码块后，内部 JSON 合法，原有 target/GPU-impact 校验也通过，仍判定 gpu_required。
- #9846：HTTP 200，finish_reason=length，completion_tokens=4000。其中 reasoning_tokens=3421、text_tokens=579，正文在 JSON 数组中途结束。原解析器报 Inference Hub response was incomplete，不是 invalid JSON。
- 8 个响应的 API JSON 结构均正常，没有缺少 choices。最大响应体 28021 字节，全部小于原有100001字节读取上限，因此本轮没有客户端读取截断。
- 历史失败响应没有保留。这些是相同输入的新复跑证据，不能逐一追认所有历史失败都出于同一原因。

## 各样本结果

| 原 PR | 原错误 | 本次分类 | finish_reason | completion tokens | body bytes |
|---|---|---|---|---:|---:|
| #8464 | Inference Hub returned invalid JSON | valid_json | stop | 1122 | 7343 |
| #9771 | Inference Hub returned invalid JSON | json_code_fence | stop | 3163 | 17762 |
| #9834 | Inference Hub returned invalid JSON | valid_json | stop | 2869 | 15679 |
| #9846 | Inference Hub returned invalid JSON | output_token_limit | length | 4000 | 28021 |
| #9894 | Inference Hub returned invalid JSON | valid_json | stop | 3233 | 20527 |
| #9916 | Inference Hub response was incomplete | valid_json | stop | 1964 | 9864 |
| #9964 | Inference Hub returned invalid JSON | valid_json | stop | 3930 | 24779 |
| #9974 | Inference Hub returned invalid JSON | valid_json | stop | 2592 | 14771 |

## 用同一返回验证最小修复

只剥掉一个完整外层 JSON 代码块，不修改内部内容。#9771 的同一份返回通过原有 pinned-tree/目标/证据校验，结果为 gpu_required，目标 tests/attention/test_attention_ts_decode_mixed_precision.py。没有自动授予 CPU 免测。详情见 normalization-verification.json。

## 其他观察

本轮所有请求最初均因 temperature 参数已弃用返回 HTTP 400；原代码已有删除 temperature 后重试的逻辑，随后获得 HTTP 200。#9974 还出现一次网络超时，原有重试后成功。这些事件与最终 JSON 格式错误分别记录。

## GitHub Actions 状态

仓库 enabled=true、allowed_actions=all，workflow active；已执行重新启用及无活动任务时的关闭/开启复位，配置保持启用。执行 API 仍返回 HTTP 422 Actions has been disabled for this repository。未更改预算或付款设置，未把该错误当作 Hub 或模型错误。实验没有运行 GPU 测试，也未修改主仓库和原有 demo PR。
