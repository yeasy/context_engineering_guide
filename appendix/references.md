# 附录 D：参考文献

本文档列出了书中引用的学术论文和关键技术报告，供读者深入研读。

## 学术论文

### 基础架构

- **Attention Is All You Need**: Vaswani, A., et al. (2017). [Attention Is All You Need](https://arxiv.org/abs/1706.03762). NIPS.
  - *解读：Transformer 架构的奠基之作，理解 Self-Attention 机制的必读文献。*

### 检索增强生成

- **RAG**: Lewis, P., et al. (2020). [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401). NeurIPS.
  - *解读：RAG 概念的开山之作，提出了将检索器与生成器端到端联合训练的范式。*

- **Self-RAG**: Asai, A., et al. (2023). [Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection](https://arxiv.org/abs/2310.11511). ICLR 2024.
  - *解读：让模型自主决定何时检索、并对自身生成结果进行反思与评估，是 Agentic RAG 的重要基础。*

- **CRAG**: Yan, S., et al. (2024). [Corrective Retrieval Augmented Generation](https://arxiv.org/abs/2401.15884).
  - *解读：引入检索评估器与纠正机制，当检索结果不可靠时触发查询改写或网页搜索，提升 RAG 鲁棒性。*

- **REPLUG**: Shi, W., et al. (2023). [REPLUG: Retrieval-Augmented Black-Box Language Models](https://arxiv.org/abs/2301.12652).
  - *解读：探讨了如何将检索器视为黑盒模型的插件进行优化。*

### 长上下文与注意力

- **Lost in the Middle**: Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2023). [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172). arXiv preprint arXiv:2307.03172.
  - *解读：揭示了模型在处理长上下文时，倾向于关注开头和结尾的信息，而忽略中间部分。*

### 知识图谱与 Graph RAG

- **Graph RAG**: Edge, D., et al. (2024). [From Local to Global: A Graph RAG Approach to Query-Focused Summarization](https://arxiv.org/abs/2404.16130).
  - *解读：微软提出的 Graph RAG 方法，通过构建社区层级的知识图谱来支持全局性摘要问答，突破了传统 RAG 在全局查询上的局限。*

### 智能体与记忆

- **MemGPT**: Packer, C., et al. (2023). [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560).
  - *解读：提出将上下文窗口视为“主内存”、外部存储视为“磁盘”的操作系统隐喻，通过虚拟上下文管理实现无限对话记忆。*

- **Generative Agents**: Park, J. S., et al. (2023). [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442). UIST 2023.
  - *解读：斯坦福的生成式智能体研究，展示了如何通过反思（Reflection）和记忆检索构建具有可信行为的智能体。*

- **Reflexion**: Shinn, N., et al. (2023). [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366). NeurIPS 2023.
  - *解读：让智能体通过语言化的自我反思进行学习，将失败经验转化为长期记忆，提升后续任务的成功率。*

- **ReAct**: Yao, S., et al. (2023). [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629). ICLR 2023.
  - *解读：提出“思考-行动-观察”的交替循环模式，是现代智能体架构的核心范式。*

### 工具使用

- **Toolformer**: Schick, T., et al. (2023). [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761).
  - *解读：展示了语言模型如何自主学习调用外部工具（计算器、搜索引擎等），是理解工具调用机制的重要文献。*

## 技术报告与基准测试

- **LongBench**: Bai, Y., et al. (2023). [LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding](https://arxiv.org/abs/2308.14508).
  - *解读：专门针对长上下文能力的评测基准。*

- **RAGAS**: Es, S., et al. (2023). [RAGAS: Automated Evaluation of Retrieval Augmented Generation](https://arxiv.org/abs/2309.15217).
  - *解读：RAG 系统的自动化评估框架，提出了忠实度、答案相关性、上下文精确度等核心指标。*

- **MTEB**: Muennighoff, N., et al. (2023). [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316). EACL 2023.
  - *解读：大规模文本嵌入基准，覆盖 8 类任务、58 个数据集，是嵌入模型选型的权威排行榜。*
