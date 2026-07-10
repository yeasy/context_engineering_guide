# 附录 E：快变事实核验表

> `verified_at`: 2026-07-10 · `expires_at`: 2026-08-09 · `ttl_days`: 30

本表是模型名称、可用性、上下文窗口、价格、协议和运行时等高波动事实的单一快照。正文只说明稳定的选型方法；需要具体型号或数值时链接到这里。到期后必须重新打开官方入口核验，不得只改日期。

## E.1 当前模型快照

<!-- volatile-status: id=openai-models status=current -->

| 厂商 | 当前官方状态 | 上下文工程含义 | 官方入口 |
| --- | --- | --- | --- |
| OpenAI | 官方模型目录将 GPT-5.5 列为生产 API 的推荐旗舰模型；GPT-5.6 是仅向部分受信合作方开放的 preview。GPT-5.3-Codex 的上下文窗口为 400K，最大输出为 128K。 | 生产默认与受限 preview 分开评估；编码智能体应使用具体模型 ID 做长上下文回归。 | [OpenAI Models](https://developers.openai.com/api/docs/models), [GPT-5.3-Codex](https://developers.openai.com/api/docs/models/gpt-5.3-codex) |
| Anthropic | Claude Fable 5 已恢复全球访问；Claude Mythos 5 仅恢复给部分美国机构；Claude Sonnet 5 已面向所有 Claude 套餐和 API 发布。 | 访问状态必须和能力规格同时核验；不得沿用已撤销的暂停公告，也不能把 Mythos 5 写成全面可用。 | [Claude Models](https://platform.claude.com/docs/en/about-claude/models/overview), [Fable 5 access restored](https://www.anthropic.com/news/redeploying-fable-5), [Claude Sonnet 5](https://www.anthropic.com/news/claude-sonnet-5), [Claude context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows) |
| Google | Gemini 3.5 Flash 使用稳定模型 ID `gemini-3.5-flash`，输入上限为 1,048,576 tokens，输出上限为 65,536 tokens。 | 固定稳定模型 ID，并在迁移时重新检查 token limits、弃用状态和区域可用性。 | [Gemini 3.5 Flash](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash), [Gemini API changelog](https://ai.google.dev/gemini-api/docs/changelog) |

<!-- volatile-status: id=anthropic-fable-access status=resolved-conflict -->

## E.2 冲突记录

| 主题 | 旧来源 | 新来源 | 处置 |
| --- | --- | --- | --- |
| Claude Fable 5 / Mythos 5 访问状态 | Anthropic 在 2026-06-12 发布过[暂停访问公告](https://www.anthropic.com/news/fable-mythos-access)。 | Anthropic 在 2026-07-01 宣布出口管制已解除，并[恢复 Fable 5 的全球访问](https://www.anthropic.com/news/redeploying-fable-5)；当前模型文档注明 Mythos 5 仅恢复给部分美国机构。 | 标记为 `resolved-conflict`；正文采用新来源，不删除旧事件，以免后来维护者误把旧公告当成当前状态。 |

## E.3 其他快变事实入口

| 类别 | 权威入口 | 编辑要求 |
| --- | --- | --- |
| 模型价格与缓存 | OpenAI、Anthropic、Google 官方 pricing | 成本示例必须标明模型 ID、区域、缓存和批处理假设，不把示例收益写成保证。 |
| MCP 与工具运行时 | [MCP Specification](https://modelcontextprotocol.io/specification), [MCP Roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/) | 记录实际解析到的规范版本；字段与该版本绑定。 |
| Agent SDK 与编码智能体 | 各厂商官方开发者文档 | 不把某产品的内部实现写成跨平台规律。 |
| Benchmark 与评估 | 官方论文和 benchmark 仓库 | 记录日期、数据集、配置和失败样例；不把单一榜单写成生产承诺。 |

## E.4 更新规则

1. 每个快变主题都必须有 `volatile-status` 标记；允许 `current` 和 `resolved-conflict`，`open-conflict` 会让项目检查失败。
2. `verified_at` 不能晚于检查日期，`expires_at` 必须等于 `verified_at + 30 天`；到期当天仍可使用，次日开始失败。
3. 有冲突时保留新旧官方来源、时间顺序和处置理由。只有能解释冲突的新证据才可标记为 `resolved-conflict`。
4. 更新本表时同步检查 [2.4 主流模型的上下文能力对比](../02_llm_basics/2.4_model_comparison.md)，避免正文复制过期参数。
