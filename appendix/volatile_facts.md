# 附录 E：快变事实核验表

> Last verified: 2026-05-18. 本表约束上下文窗口、模型价格、协议、RAG/Agent runtime 等高波动事实。

| 类别 | 当前维护口径 | 权威入口 | 编辑要求 |
| --- | --- | --- | --- |
| 模型上下文窗口 | OpenAI、Claude、Gemini、Llama、DeepSeek 等上下文窗口只写 dated snapshot。 | [OpenAI Models](https://developers.openai.com/api/docs/models/all/), [Claude Models](https://platform.claude.com/docs/en/about-claude/models/overview), [Gemini Models](https://ai.google.dev/gemini-api/docs/models) | 正文应强调设计策略，具体窗口放表格并标日期。 |
| 成本与缓存 | token 单价、prompt cache、batch、long context 价格以官方 pricing 为准。 | OpenAI / Anthropic / Google 官方 pricing | ROI 示例必须标注假设，不写成通用收益。 |
| MCP / tool runtime | MCP transport、OAuth、server/client 能力以规范版本为准。 | [MCP Spec](https://modelcontextprotocol.io/specification), [MCP Roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/) | 协议字段必须跟规范版本绑定。 |
| Agent SDK / coding agent | Claude Code、OpenAI Agents、Codex、Gemini tooling 以官方文档为准。 | 各厂商官方 developer docs | 不把某产品内部实现写成通用事实。 |
| Benchmark / eval | 长上下文、RAG、Agent benchmark 只作为 dated snapshot。 | 官方论文、benchmark 仓库 | 避免把单一榜单当生产效果承诺。 |
