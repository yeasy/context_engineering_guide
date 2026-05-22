# EnterpriseKnow 可运行最小实验

本目录把第 14 章的企业知识库问答案例落成一个本地可运行实验。它只依赖 Python 标准库，用小样本文档演示以下闭环：

- 文档读取、元数据解析和分块。
- 混合检索：BM25 稀疏检索 + 本地向量相似度近似。
- 权限过滤：按部门隔离受限知识。
- 上下文组装：控制上下文大小并保留来源。
- 带引用回答：只基于检索片段生成答案。
- 评估集回归：检查来源命中和答案关键项。

## 快速运行

在仓库根目录执行：

```bash
python3 examples/enterprise_know/enterprise_know.py --query "差旅报销需要在多久内提交？"
```

运行评估集：

```bash
python3 examples/enterprise_know/enterprise_know.py --eval
python3 -m unittest examples/enterprise_know/test_enterprise_know.py
```

## 文件说明

| 文件 | 作用 |
|------|------|
| `enterprise_know.py` | 本地 RAG 管道、检索器、答案生成和评估入口 |
| `sample_docs/` | 示例知识库文档，含简单 ACL 元数据 |
| `eval_set.jsonl` | 最小回归评估集 |
| `test_enterprise_know.py` | 单元测试，覆盖检索、ACL、引用和评估 |

## 生产化差距

这个实验故意保持小而透明，适合解释第 14 章的接口边界。真实生产系统还需要替换或补齐：

- 领域嵌入模型、重排序模型和持久化向量库。
- 文档解析流水线、版本化索引和回滚流程。
- 租户级权限系统、审计日志、DLP 和密钥管理。
- 线上可观测性、SLO 告警和事故响应手册。
- 更大的黄金评估集、人工抽检和分场景阈值。
