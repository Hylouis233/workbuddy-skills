---
name: wegene-gip
display_name: GIP 靶点解读
display_name_en: GIP target interpretation
description: Run the local WeGene GIP target interpretation lightweight app and explain its genotype report. Use when the user asks to interpret, test, or package this WeGene app.
description_zh: 运行本目录里的 WeGene「GIP 靶点解读」轻应用，解释合成基因型的 Markdown 报告。用户要求解读、测试或打包该应用时使用。
description_en: Run the bundled WeGene GIP target interpretation app on a synthetic genotype and explain the Markdown report.
category: data-analysis
version: 1.0.0
author: Hylouis233
allowed-tools: Bash,Read
---

# GIP 靶点解读

GIPR 靶点基因解读 WeGene 轻应用

这个技能只运行本目录 `scripts/` 里的轻应用。它不读取真实个人基因组，也不构成诊断、用药或医疗建议。

## 运行

在 `scripts/` 目录执行，让 `main.py` 能导入同目录模块：

```bash
cd scripts
python main.py < test_wildtype.json
```

如果该目录没有 `test_wildtype.json`，改用目录里已有的 `test_*.json` 或 `demo.json`。输入是合成基因型 JSON，不要把真实检测原始数据写进命令或报告。

## 回答

- 先给应用结论，再列所用位点和基因型。
- 基因型、频率和文献只引用脚本与 README 里已经写明的内容。脚本没有的 rsID 或 PMID 不要补造。
- 保留应用原文里的免责声明：结果仅供研究参考，不构成医疗建议。
- 需要打包时，把 `scripts/` 下的 `main.py`、`gene_data.py`、`interpretation.py`、`report_generator.py`、`requirements.txt` 打进 zip 根目录，不要包含测试 JSON、图片或上级目录。
