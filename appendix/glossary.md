# 附录 A：术语表

本术语表收录了上下文工程领域的核心术语及其定义。

---

## 术语列表

### A

**Agentic [RAG](../05_select/5.1_rag_principles.md)（自主型 RAG）**  
智能体自主决定检索时机、策略和内容的[检索增强生成](../05_select/5.1_rag_principles.md)模式。

**ANN（近似最近邻）**  
Approximate Nearest Neighbor，向量搜索中用于快速查找相似向量的算法。

### C

**Chunking（分块）**  
将长文档切分为较小片段的过程，是 RAG 系统的关键步骤。

**Context Engineering（上下文工程）**  
设计、组织、优化和管理大语言模型信息环境的系统性工程学科。

**Context Window（上下文窗口）**  
大语言模型一次能处理的最大 Token 序列长度。

**Cross-Encoder（交叉编码器）**  
将查询和文档同时输入模型进行相关性评分的重排序技术。

### E

**Embedding（嵌入）**  
将文本转换为数值向量的过程，使语义相似的文本在向量空间中距离相近。

**Episodic Memory（情景记忆）**  
存储具体事件和经历的记忆类型。

### F

**Function Calling（函数调用）**  
模型生成结构化函数调用请求的能力，用于与外部工具交互。

### G

**Graph RAG（图检索增强生成）**  
结合知识图谱进行检索和推理的 RAG 变体。

### H

**Hallucination（幻觉）**  
模型生成与事实不符或缺乏依据的内容的现象。

**HNSW**  
Hierarchical Navigable Small World，高效的向量索引算法。

**Hybrid Search（混合检索）**  
结合语义检索和关键词检索的混合方法。

### K

**KV Cache**  
Key-Value 缓存，存储生成过程中 Token 的键值向量以避免重复计算。

### L

**LLM（大语言模型）**  
Large Language Model，基于 Transformer 架构的大规模预训练语言模型。

### M

**MCP（Model Context Protocol）**  
Anthropic 提出的 AI 模型与外部工具交互的标准协议。

**Memory Architecture（记忆架构）**  
组织和管理 AI 系统记忆的多层次结构设计。

### P

**Prompt Engineering（提示词工程）**  
设计和优化输入给模型的文本指令的技术，是上下文工程的子集。

### R

**RAG（检索增强生成）**  
Retrieval-Augmented Generation，结合信息检索与语言模型生成的技术。

**[ReAct](../09_agents/9.1_agent_architecture.md)**  
Reason + Act，结合推理和行动的智能体运行模式。

**Reranking（重排序）**  
对初步检索结果进行二次排序以优化相关性的技术。

**RRF（倒数排名融合）**  
Reciprocal Rank Fusion，融合多个检索结果排序的算法。

### S

**Semantic Memory（语义记忆）**  
存储抽象事实和概念的记忆类型。

**Semantic Search（语义搜索）**  
基于语义相似度而非关键词匹配的信息检索方法。

**System Prompt（系统提示词）**  
定义模型基本角色和行为的核心指令。

### T

**Token**  
大语言模型处理文本的基本单位。

**Tokenizer（分词器）**  
将文本转换为 Token 序列的组件。

**Transformer**  
现代大语言模型的基础架构，基于自注意力机制。

### V

**Vector Database（向量数据库）**  
专门优化用于存储和检索高维向量的数据库系统。

### W

**Working Memory（工作记忆）**  
对应上下文窗口，存储当前任务即时信息的短期记忆。
