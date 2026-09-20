# 附录 E：快变事实核验表

> `verified_at`: 2026-09-20 · `expires_at`: 2026-10-20 · `ttl_days`: 30

本表是模型名称、可用性、上下文窗口、价格、协议和运行时等高波动事实的单一快照。正文只说明稳定的选型方法；需要具体型号或数值时链接到这里。到期后必须重新打开官方入口核验，不得只改日期。

## E.1 当前模型快照

<!-- volatile-status: id=openai-models status=current -->

| 厂商 | 当前官方状态 | 上下文工程含义 | 官方入口 |
| --- | --- | --- | --- |
| OpenAI | 当前模型目录已把 **GPT-6 Astra（`gpt-6-astra`）** 列在首位并标为 **Default**，目录开篇直接写「不确定从哪开始就用 GPT-6 Astra，我们的旗舰模型」；模型页已无任何受限访问表述，Tier 1–5 速率限制齐备，$10/$50、1,050,000 上下文、128K 输出、知识截止 2026-04-30，即**已全量可用**（本行上一版写的是「正向 Trusted Access Program 滚动开放、尚未全量可用」，那是 2026-09-03 刚发布时的状态，不要改回去）。其下 GPT-5.6 Sol 仍为全量可用的复杂推理和编码档（$4/$20），GPT-5.6 Terra 用于平衡智能与成本，GPT-5.6 Luna 面向成本敏感的高吞吐工作负载。2026-07-09 的 API changelog 记录三者已发布到 Responses、Chat Completions 和 Batch API。GPT-5.3-Codex 的上下文窗口为 400K，最大输出为 128K，且在 Astra 发布后官方仍称其为迄今最强的智能体编码模型。 | 按 Sol、Terra、Luna 的能力与成本边界选型，并用具体模型 ID、账号层级和实际区域做上线前回归；编码智能体仍需单独评估 GPT-5.3-Codex。 | [OpenAI Models](https://developers.openai.com/api/docs/models), [GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol), [GPT-5.6 Terra](https://developers.openai.com/api/docs/models/gpt-5.6-terra), [GPT-5.6 Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna), [API changelog](https://developers.openai.com/api/docs/changelog), [GPT-5.3-Codex](https://developers.openai.com/api/docs/models/gpt-5.3-codex), [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra) |
| Anthropic | **2026-09-01 发布的 Claude Fable 5.1（`claude-fable-5-1`）与 Claude Mythos 5.1 已进入当前阵容**：官方模型总览页把 Fable 5.1 定位为「demanding reasoning and long-horizon agentic work」，Opus 5 仍是「不确定选哪个时的起点」；Mythos 5.1 与 Mythos 5 一样在定价页标注 limited availability。Claude Fable 5 曾恢复全球访问，官方一度称其为「能力最强的广泛发布模型」，现已随 5.1 发布移入 Legacy；Claude Mythos 5 非普遍可用，仅通过 Project Glasswing 向获批客户受限开放；Claude Sonnet 5 已面向所有 Claude 套餐和 API 发布。**Claude Opus 5（`claude-opus-5`）已于 2026-07-24 发布**，官方模型页把它列为「不确定选哪个时的起点」（面向复杂智能体编码与企业场景，$5/$25、1M 上下文、128K 输出）。同一页的 Legacy 区间现已扩为 **Fable 5、Opus 4.8、Opus 4.7、Opus 4.6、Opus 4.5、Sonnet 4.6 与 Sonnet 4.5**（仍可用，但建议迁移）；Haiku 4.5 仍属当前模型，不在该区间内。 | 访问状态必须和能力规格同时核验；不得沿用已撤销的暂停公告，也不能把 Mythos 5 写成全面可用；**也不要再把 Opus 4.8 写成当前旗舰**——它的价格和窗口没变，变的是它在官方目录中的位置；**同理不要再把 Fable 5 写成当前最强推理档**，该位置已是 Fable 5.1。Mythos 系列的受限状态只在定价页有明文标注、模型总览页不列，核验时两页都要看。 | [Claude Models](https://platform.claude.com/docs/en/models/overview), [Fable 5 access restored](https://www.anthropic.com/news/redeploying-fable-5), [Claude Sonnet 5](https://www.anthropic.com/news/claude-sonnet-5), [Claude context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows), [Claude Pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Google | 稳定 Flash 序列的最新一档是 **Gemini 3.8 Flash（`gemini-3.8-flash`，2026-09-02 GA，模型页标注 New Stable）**，输入上限 1,048,576 tokens、输出上限 65,536 tokens，官方描述为「最智能的 Flash 模型」；其下 3.7 Flash（2026-08-13 GA）与 3.6 Flash（2026-07-21 GA）均为 Stable，但官方已把两者描述为上一代；更早的 `gemini-3.5-flash` 仍为 Stable，官方描述已降为 **legacy（旧版）Flash 模型**。Pro 一档仍只有 Preview 的 `gemini-3.1-pro-preview`，I/O 上预告的 3.5 Pro 至今未进入目录。 | 固定稳定模型 ID，并在迁移时重新检查 token limits、弃用状态和区域可用性。 | [Gemini 3.8 Flash](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash), [Gemini 3.5 Flash](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash), [Gemini API changelog](https://ai.google.dev/gemini-api/docs/changelog) |

## E.2 冲突记录

<!-- volatile-status: id=openai-gpt-5-6-availability status=resolved-conflict -->
<!-- volatile-status: id=anthropic-fable-access status=resolved-conflict -->

| 主题 | 旧来源 | 新来源 | 处置 |
| --- | --- | --- | --- |
| GPT-5.6 API 可用性 | OpenAI 在 2026-06-26 的[预览公告](https://openai.com/index/previewing-gpt-5-6-sol/)中说明 Sol、Terra、Luna 仅向少量受信合作方开放，这是发布初期的旧快照。 | 后续的 [2026-07-09 API changelog](https://developers.openai.com/api/docs/changelog)明确记录三者已发布到 Responses、Chat Completions 和 Batch API；当前[模型目录](https://developers.openai.com/api/docs/models)将 Sol 列为旗舰并链接三款模型，当前[可用性说明](https://help.openai.com/en/articles/20001354)也列出 OpenAI API 可用 Sol、Terra 和 Luna。 | 标记为 `resolved-conflict`；以后续带日期的 API 发布记录和当前目录取代旧 preview 公告作为当前 API 状态依据，同时保留旧公告说明时序。ChatGPT 的套餐资格和渐进发布仍按当前帮助页与实际账号核验。 |
| Claude Fable 5 / Mythos 5 访问状态 | Anthropic 在 2026-06-12 发布过[暂停访问公告](https://www.anthropic.com/news/fable-mythos-access)。 | 2026-07-01 的恢复公告先恢复给一组美国机构，并[恢复 Fable 5 的全球访问](https://www.anthropic.com/news/redeploying-fable-5)；当前模型文档明确 Mythos 5 非普遍可用，仅通过 Project Glasswing 向获批客户受限开放。 | 标记为 `resolved-conflict`；正文采用当前来源，同时保留 7 月 1 日的历史恢复范围，避免后来维护者误把中间状态或旧暂停公告当成当前状态。 |

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
