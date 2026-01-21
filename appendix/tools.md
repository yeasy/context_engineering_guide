# 附录 B：常用工具与框架

本附录介绍上下文工程实践中常用的工具和框架。

---

## RAG 框架

### LangChain

**简介**：最流行的 LLM 应用开发框架之一，提供全面的 RAG 支持。

**特点**：
- 丰富的组件和集成
- 活跃的社区
- 详细的文档

**官网**：https://langchain.com

### LlamaIndex

**简介**：专注于数据索引和检索的 LLM 框架。

**特点**：
- 多种索引结构
- 灵活的检索策略
- 支持 Graph RAG

**官网**：https://llamaindex.ai

### Haystack

**简介**：端到端 NLP 框架，支持构建完整的 RAG 管道。

**特点**：
- 生产级就绪
- 可视化管道编辑
- 评估工具集成

**官网**：https://haystack.deepset.ai

---

## 向量数据库

### Pinecone

**类型**：全托管云服务

**特点**：开箱即用、免运维、快速启动

### Weaviate

**类型**：开源/云服务

**特点**：功能丰富、GraphQL API、支持混合搜索

### Milvus

**类型**：开源

**特点**：高性能、可扩展、适合大规模部署

### Qdrant

**类型**：开源

**特点**：Rust 实现、高性能、轻量级

### Chroma

**类型**：开源

**特点**：嵌入式、简单易用、适合原型开发

### pgvector

**类型**：PostgreSQL 扩展

**特点**：与现有 PG 基础设施集成

---

## 嵌入模型

### 商业服务

| 服务 | 模型 | 特点 |
|------|------|------|
| OpenAI | text-embedding-3 | 质量高、易集成 |
| Cohere | Embed v3 | 多语言、长上下文 |
| Google | Vertex Embeddings | 多模态支持 |

### 开源模型

| 模型 | 维度 | 特点 |
|------|------|------|
| BGE 系列 | 1024 | 中文优秀、多语言 |
| E5 系列 | 1024 | 指令式嵌入 |
| sentence-transformers | 变化 | 丰富选择 |

---

## 评估工具

### RAGAS

评估 RAG 系统质量的自动化框架。

### TruLens

RAG 应用的监控和评估平台。

### DeepEval

LLM 应用的评估框架。

---

## 可观测性

### LangSmith

LangChain 配套的追踪和监控平台。

### Weights & Biases

机器学习实验跟踪，支持 LLM 应用。

### Arize

模型监控和可观测性平台。

---

## MCP 相关

### MCP SDK

官方提供的 MCP 协议开发工具包。

### 预构建 MCP 服务

- 文件系统服务
- 数据库服务
- 网页爬取服务
- 各种 API 集成

---

## 选型建议

| 场景 | 推荐选择 |
|------|----------|
| 快速原型 | LangChain + Chroma |
| 生产部署 | LlamaIndex/LangChain + Pinecone/Milvus |
| 企业集成 | pgvector + 现有基础设施 |
| 研究实验 | 开源模型 + 开源数据库 |
