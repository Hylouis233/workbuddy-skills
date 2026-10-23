<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-03-05 | Updated: 2026-03-21 -->

# men2-snps

## Purpose
MEN2 (多发性内分泌腺瘤病2型) RET 基因 SNP 筛查轻应用。用于筛查用户基因组数据中与 MEN2 相关的 RET 基因致病突变，评估甲状腺髓样癌 (MTC) 风险。MEN2 是由 RET 原癌基因胚系突变引起的常染色体显性遗传病，与 GLP-1/GIP/GCG 类药物的黑框警告高度相关。

## Key Files
| File | Description |
|------|-------------|
| `main.py` | 主程序入口，处理 stdin JSON 输入，输出 Markdown 报告 |
| `gene_data.py` | RET 基因变异定义，包含 18 个已验证 SNP 位点 |
| `interpretation.py` | 风险解读逻辑，ATA 风险分级算法 |
| `report_generator.py` | Markdown 报告生成器 |
| `MEN2_RET_SNPs.json` | SNP 位点数据（JSON 格式） |
| `MEN2_RET_SNPs.md` | SNP rs 号汇总表（参考文献） |
| `VERIFICATION_REPORT.md` | SNP rs 号验证报告 |
| `wegene_app_config.json` | WeGene 轻应用配置（v1.1.0） |
| `requirements.txt` | 依赖声明（无外部依赖） |

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| 无 | 独立应用，无子目录 |

## For AI Agents

### Working In This Directory
- 完整的 MEN2 风险筛查轻应用，可直接部署
- 已删除错误的 rs 号 (rs77877000, rs75063161)
- 争议性变异 Y791F 已标注为 Uncertain/VUS

### Testing Requirements
```bash
# 测试 MEN2A 场景
cat test_men2a.json | python -X utf8 main.py

# 测试 MEN2B 场景
cat test_men2b.json | python -X utf8 main.py

# 测试正常场景
cat test_normal.json | python -X utf8 main.py
```

### Common Patterns
```python
# 基因型处理
genotype = ''.join(sorted(inputs.get('RS74799832', '--').upper()))

# 风险等级判断
if variant['ata_risk'] == 'ATA-HST':
    priority = '紧急'
```

### SNP 风险分类

| 风险等级 | 亚型 | 代表突变 | 手术建议 |
|----------|------|----------|----------|
| 最高风险 (ATA-HST) | MEN2B | M918T, A883F | <6月龄 |
| 高风险 (ATA-H) | MEN2A | C634R/Y/W/S | 3-5岁 |
| 中等风险 (ATA-MOD) | MEN2A/FMTC | C609-C620, V804M/L | 根据降钙素调整 |
| 低风险 (ATA-MOD) | FMTC | E768D, L790F, S891A | 可延迟 |

### 已验证的 SNP 数量 (2026-03-09 修复后)
- 总变异数：**18** (已删除 2 个错误 rs 号)
- 已验证：16
- 争议性：1 (Y791F - 保留但标注)
- 错误已删除：rs77877000 (C634F), rs75063161 (C634G)

## Dependencies

### Internal
- 依赖 WeGene 轻应用框架
- 需要 `wegene_utils.py` 或 `wegene_utils.R` 工具库

### External
- 数据来源：
  - ClinVar: https://www.ncbi.nlm.nih.gov/clinvar
  - dbSNP: https://www.ncbi.nlm.nih.gov/snp
  - ATA 2015 Guidelines
  - OMIM (MEN2A: #171400, MEN2B: #162300)

<!-- MANUAL: Custom project notes can be added below -->
