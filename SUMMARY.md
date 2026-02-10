# Summary

* [前言](README.md)

## 第一部分：认识上下文工程

* [第一章：上下文工程概述](01_overview/README.md)
  * [1.1 什么是上下文工程](01_overview/1.1_definition.md)
  * [1.2 从提示词工程到上下文工程](01_overview/1.2_evolution.md)
  * [1.3 上下文工程的核心价值](01_overview/1.3_value.md)
  * [1.4 本书结构与学习路径](01_overview/1.4_roadmap.md)
  * [本章小结](01_overview/summary.md)

* [第二章：大模型基础与上下文窗口](02_llm_basics/README.md)
  * [2.1 大语言模型工作原理](02_llm_basics/2.1_how_llm_works.md)
  * [2.2 上下文窗口的本质](02_llm_basics/2.2_context_window.md)
  * [2.3 Token 与上下文限制](02_llm_basics/2.3_tokens.md)
  * [2.4 主流模型的上下文能力对比](02_llm_basics/2.4_model_comparison.md)
  * [本章小结](02_llm_basics/summary.md)

* [第三章：上下文工程的理论框架](03_framework/README.md)
  * [3.1 信息环境设计原则](03_framework/3.1_design_principles.md)
  * [3.2 四大核心策略概览](03_framework/3.2_four_strategies.md)
  * [3.3 上下文质量评估](03_framework/3.3_quality_metrics.md)
  * [3.4 上下文工程方法论](03_framework/3.4_methodology.md)
  * [本章小结](03_framework/summary.md)

## 第二部分：核心技术与策略

* [第四章：上下文写入与存储](04_write/README.md)
  * [4.1 外部存储与记忆系统](04_write/4.1_external_storage.md)
  * [4.2 记忆架构设计](04_write/4.2_memory_architecture.md)
  * [4.3 知识库构建与管理](04_write/4.3_knowledge_base.md)
  * [4.4 向量数据库实践](04_write/4.4_vector_database.md)
  * [本章小结](04_write/summary.md)

* [第五章：上下文选择与检索](05_select/README.md)
  * [5.1 检索增强生成原理](05_select/5.1_rag_principles.md)
  * [5.2 文档分块策略](05_select/5.2_chunking.md)
  * [5.3 嵌入模型与语义搜索](05_select/5.3_embeddings.md)
  * [5.4 重排序与相关性优化](05_select/5.4_reranking.md)
  * [5.5 混合检索与高级 RAG](05_select/5.5_advanced_rag.md)
  * [本章小结](05_select/summary.md)

* [第六章：上下文压缩与优化](06_compress/README.md)
  * [6.1 信息密度与压缩原理](06_compress/6.1_compression_principles.md)
  * [6.2 摘要与信息提取](06_compress/6.2_summarization.md)
  * [6.3 对话历史管理](06_compress/6.3_conversation_history.md)
  * [6.4 上下文窗口优化策略](06_compress/6.4_window_optimization.md)
  * [6.5 压缩策略案例分析](06_compress/6.5_compression_cases.md)
  * [本章小结](06_compress/summary.md)

* [第七章：上下文隔离与结构化](07_isolate/README.md)
  * [7.1 结构化上下文设计](07_isolate/7.1_structured_context.md)
  * [7.2 XML 标签与指令分层](07_isolate/7.2_xml_tags.md)
  * [7.3 系统提示词设计](07_isolate/7.3_system_prompts.md)
  * [7.4 多任务上下文隔离](07_isolate/7.4_task_isolation.md)
  * [7.5 隔离策略案例分析](07_isolate/7.5_isolation_cases.md)
  * [本章小结](07_isolate/summary.md)

## 第三部分：进阶技术与架构

* [第八章：工具调用与能力扩展](08_tools/README.md)
  * [8.1 函数调用机制](08_tools/8.1_function_calling.md)
  * [8.2 工具定义与设计](08_tools/8.2_tool_design.md)
  * [8.3 工具执行与结果处理](08_tools/8.3_tool_execution.md)
  * [8.4 MCP 协议与工具标准化](08_tools/8.4_mcp_protocol.md)
  * [本章小结](08_tools/summary.md)

* [第九章：智能体上下文管理](09_agents/README.md)
  * [9.1 智能体架构与上下文](09_agents/9.1_agent_architecture.md)
  * [9.2 单智能体上下文管理](09_agents/9.2_single_agent.md)
  * [9.3 多智能体上下文传递](09_agents/9.3_multi_agent.md)
  * [9.4 智能体记忆与学习](09_agents/9.4_agent_memory.md)
  * [本章小结](09_agents/summary.md)

* [第十章：进阶 RAG 与自适应上下文](10_advanced/README.md)
  * [10.1 Agentic RAG 与自主检索](10_advanced/10.1_agentic_rag.md)
  * [10.2 Graph RAG 与知识图谱](10_advanced/10.2_graph_rag.md)
  * [10.3 自适应上下文管理](10_advanced/10.3_adaptive_context.md)
  * [10.4 长上下文模型应用](10_advanced/10.4_long_context.md)
  * [10.5 多模态上下文管理](10_advanced/10.5_multimodal_context.md)
  * [本章小结](10_advanced/summary.md)

* [第十一章：反模式与常见陷阱](11_antipatterns/README.md)
  * [11.1 过度压缩与信息丢失](11_antipatterns/11.1_over_compression.md)
  * [11.2 上下文污染与隔离失效](11_antipatterns/11.2_context_pollution.md)
  * [11.3 检索失败与相关性陷阱](11_antipatterns/11.3_retrieval_failures.md)
  * [本章小结](11_antipatterns/summary.md)

## 第四部分：工程实战与未来演进

* [第十二章：生产环境最佳实践](12_production/README.md)
  * [12.1 上下文工程工作流](12_production/12.1_workflow.md)
  * [12.2 性能优化与成本控制](12_production/12.2_optimization.md)
  * [12.3 可观测性与调试](12_production/12.3_observability.md)
  * [12.4 安全性与治理](12_production/12.4_security.md)
  * [12.5 故障排查与问题诊断](12_production/12.5_troubleshooting.md)
  * [本章小结](12_production/summary.md)

* [第十三章：行业应用案例](13_cases/README.md)
  * [13.1 医疗：电子病历智能问答](13_cases/13.1_medical.md)
  * [13.2 金融：智能风控知识库](13_cases/13.2_financial.md)
  * [13.3 法律：合同审查助手](13_cases/13.3_legal.md)
  * [13.4 教育：个性化助教系统](13_cases/13.4_education.md)
  * [13.5 案例分析：Manus AI 的全自主智能体架构](13_cases/13.5_manus_agent.md)
  * [本章小结](13_cases/summary.md)

* [第十四章：综合实战 - 构建企业知识库问答系统](14_practice/README.md)
  * [14.1 项目需求与架构设计](14_practice/14.1_requirements.md)
  * [14.2 知识库构建与向量化](14_practice/14.2_knowledge_base.md)
  * [14.3 检索系统实现](14_practice/14.3_retrieval.md)
  * [14.4 对话历史管理](14_practice/14.4_history.md)
  * [14.5 性能优化与部署](14_practice/14.5_optimization.md)
  * [14.6 持续迭代与改进](14_practice/14.6_iteration.md)
  * [本章小结](14_practice/summary.md)

* [第十五章：未来展望与发展趋势](15_future/README.md)
  * [15.1 上下文工程的技术演进](15_future/15.1_tech_evolution.md)
  * [15.2 行业应用趋势](15_future/15.2_industry_trends.md)
  * [15.3 挑战与机遇](15_future/15.3_challenges.md)
  * [15.4 成为上下文工程专家](15_future/15.4_becoming_expert.md)
  * [本章小结](15_future/summary.md)

## 附录

* [附录 A：术语表](appendix/glossary.md)
* [附录 B：工具与技术生态](appendix/tools.md)
* [附录 C：参考资源](appendix/resources.md)
* [附录 D：参考文献](appendix/references.md)
