# EnterpriseKnow 可运行最小实验

本目录把第 14 章的企业知识库问答案例落成一个本地可运行实验。它只依赖 Python 标准库，用小样本文档演示以下闭环：

- 文档读取、元数据解析和分块。
- 混合检索：BM25 稀疏检索 + 本地向量相似度近似。
- 权限过滤：按部门隔离受限知识。
- 上下文组装：控制上下文大小并保留来源。
- 带引用回答：只基于检索片段生成答案。
- 评估集回归：同时覆盖正例、否定提问、越权、冲突来源、信息缺失和无关问题。

## 快速运行

在仓库根目录执行：

```bash
python3 examples/enterprise_know/enterprise_know.py --query "差旅报销需要在多久内提交？"
```

输出应包含 `answer`、`context` 和 `results` 字段。`answer` 应说明差旅报销需要在完成后 30 天内提交，`results[0].source` 应指向命中的制度文档。

权限过滤可以用同一问题做对照：

```bash
python3 examples/enterprise_know/enterprise_know.py --query "生产数据库访问需要什么审批？" --department hr
python3 examples/enterprise_know/enterprise_know.py --query "生产数据库访问需要什么审批？" --department engineering
```

第一条命令应拒绝回答并返回空 `results`；第二条命令应命中 `security_access.md`，并说明生产数据库访问需要堡垒机、MFA 和已批准工单。这组对照用于确认检索阶段和回答阶段都没有绕过部门权限。

运行评估集：

```bash
python3 examples/enterprise_know/enterprise_know.py --eval
python3 -m unittest examples/enterprise_know/test_enterprise_know.py
```

评估通过时，`--eval` 输出应包含 `passed: true`，并且 `source_hit_rate`、`answer_term_hit_rate` 与 `source_precision` 都为 `1.0`。对回答类 case，`expected_sources` 表示必须命中的来源，`allowed_sources` 是检索与回答可引用来源的白名单（未填写时默认等于 `expected_sources`），`forbidden_sources` 则显式标记禁止命中的来源。任一 case 失败时命令返回非零状态；逐条报告会给出 `missing_terms`、`actual_sources`、`unexpected_sources`、`forbidden_retrieved_sources`、`cited_sources`、回答证据污染字段和 `failure_reason`，用于区分关键项缺失、来源错配、越权命中、回答污染和拒答失败。

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
