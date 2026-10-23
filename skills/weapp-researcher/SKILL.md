---
name: weapp-researcher
display_name: WeGene 轻应用研究员
display_name_en: WeGene WeApp Researcher
description: Research a disease and draft a WeGene lightweight gene-app package from dbSNP, ClinVar, and PubMed. Use when the user asks to build, research, or update a WeGene weapp for a named disease.
description_zh: 按疾病名称检索 dbSNP、ClinVar 和 PubMed，起草符合 WeGene 轻应用规范的基因解读代码包。
description_en: Research a named disease in dbSNP, ClinVar, and PubMed, then draft a WeGene lightweight app package.
category: data-analysis
version: 1.0.0
author: Hylouis233
allowed-tools: Bash,Read,WebSearch,WebFetch
---

# WeGene 轻应用研究员

用户给出疾病名称时，调研公开数据库并起草一个 WeGene 轻应用代码包。输出是草稿和来源清单，不是临床诊断，也不能直接当作医疗建议。

## 运行约束

生成的轻应用必须符合 WeGene 运行时：

- 从 stdin 读 JSON，结果只从 stdout 输出一次，错误写 stderr。
- 主文件是 `main.py` 或 `main.R`。R 脚本后缀必须是大写 `.R`。
- 部署包是 zip，根目录直接放文件，不要再套一层目录。
- 运行时限制：120 秒、代码包 10MB、输出 1MB、轻应用运行时不允许访问网络。
- 位点键使用大写 `RS` 前缀。杂合基因型在比较前按字母排序。未检出是 `--`，未检测是 `__`。

## 流程

1. 确认疾病名称。没有名称时先问，不自行换成邻近疾病。
2. 用 GeneCards、OMIM 或 PharmGKB 的公开页面列出候选基因，再收敛到有功能或药物响应文献的位点。
3. 对每个保留位点核对 dbSNP 和 ClinVar：rsID、染色体位置、等位基因、频率、临床意义、相关状况。两边冲突时并列写出，不取平均，不选一个装成已核实。
4. 用 PubMed 找该位点的功能、药物响应和人群研究。每个保留位点至少两篇独立文献，并优先近五年的论文。记录 PMID、题目、年份和期刊。数据库里查不到就写未查到，不编 PMID。
5. 写明证据等级和排除理由。纯研究用途、证据过弱、或频率低到无法解释的位点不要写进评分，可以放在排除表。
6. 设计透明评分。每个基因型对应的分数、风险分层和文献依据放在 `interpretation.py`，不要把规则散落在报告措辞里。
7. 生成下面的代码包，并用一条合成基因型从 stdin 跑通 `main.py`。测试数据不能使用真实个人基因组。

```text
output/<疾病>-weapp/
├── main.py
├── gene_data.py
├── interpretation.py
├── report_generator.py
├── requirements.txt
└── README.md
```

## 报告里必须有的内容

- 基因和位点标识，以及 dbSNP、ClinVar、PMID 来源。
- 哪些字段来自数据库，哪些是评分规则。
- 争议和未覆盖的数据库。
- 明确写：结果仅供研究参考，不构成诊断、用药或医疗建议。

## 不要做的事

- 不要编造 rsID、频率、临床意义或文献。
- 不要把 VUS 写成致病结论。
- 不要要求轻应用在运行时联网或读取本机凭证。
- 不要输出真实基因组或任何 API 密钥。
