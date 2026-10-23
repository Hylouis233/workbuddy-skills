<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-03-08 | Updated: 2026-03-21 -->

# gcgr-app

## Purpose
GCGR (gcgr-app) 是一个 WeGene 轻应用，分析 GCGR 基因 Gly40Ser (rs1801483) 变异，评估胰高血糖素受体功能和对 GIP/GLP-1/GCGR 三重激动剂（如 瑞他鲁肽）的药物响应。

## Module Overview

**Purpose**: Generate personalized genetic reports for GCGR pathway analysis.

**Input**: JSON via stdin containing GCGR genotypes
**Output**: Markdown report via stdout

---

## Architecture

```
stdin (JSON) -> main.py -> Markdown Report -> stdout
                    |
                    +-> gene_data.py (data definitions)
                    +-> interpretation.py (scoring logic)
                    +-> report_generator.py (formatting)
```

---

## Files

| File | Purpose | Lines |
|------|---------|-------|
| `main.py` | Entry point, input validation, orchestration | ~120 |
| `gene_data.py` | GCGR locus definitions, risk levels, constants | ~180 |
| `interpretation.py` | Scoring algorithm, receptor function assessment | ~250 |
| `report_generator.py` | Markdown report generation | ~280 |
| `requirements.txt` | Dependencies (none - stdlib only) | ~4 |
| `README.md` | User documentation | ~90 |

### Test Files

| File | Purpose |
|------|---------|
| `demo.json` | Standard test case |
| `test_wildtype.json` | Wild-type (GG) genotype test |
| `test_variant.json` | Variant (SS) genotype test |
| `test_heterozygous.json` | Heterozygous (GS) test |
| `test_missing.json` | Missing data handling test |

---

## Core Data Structures

### GENES Dictionary (`gene_data.py`)

GCGR Gly40Ser locus:

```python
GENES = {
    'GCGR_Gly40Ser': {  # Gly40Ser - receptor function
        'rsid': 'RS1801483',
        'hgvs_coding': 'NM_000160.5:c.118G>A',
        'hgvs_protein': 'p.Gly40Ser',
        'name': 'GCGR Gly40Ser',
        'risk_alleles': ['AA'],
        'protective_alleles': ['GG'],
        'heterozygous': ['GA', 'AG'],
        'weight': 1.0,
        'category': 'receptor_function',
        'interpretation': {...}
    }
}
```

### Scoring System

| Genotype Type | Score | Description |
|---------------|-------|-------------|
| GG (Wild-type) | 2 | Normal receptor function |
| GS (Heterozygous) | 1 | Moderate function |
| SS (Variant) | 0 | Reduced glucagon binding |
| Unknown | None | Cannot assess |

---

## Key Functions

### main.py

```python
def get_genotype_from_input(inputs, gene_key) -> str or None
def validate_input(inputs) -> (bool, str)
def process_genetic_data(inputs) -> str  # Returns Markdown report
def main()  # Entry point
```

### interpretation.py

```python
def analyze_genotypes(inputs) -> dict          # Full analysis result
def get_personalized_recommendations(results) -> list  # Health advice
```

### report_generator.py

```python
def generate_report(results, recommendations) -> str  # Full Markdown report
```

---

## Input/Output Format

### Input (stdin JSON)

```json
{
  "inputs": {
    "format": "wegene_affy_2",
    "RS1801483": "GG",
    "sex": 1,
    "age": 35
  }
}
```

### Output (stdout Markdown)

Structured report with:
1. 基因概览 (Gene Overview)
2. 综合评估 (Comprehensive Assessment)
3. 详细位点解读 (Detailed Interpretation)
4. 人群特异性说明 (Population Specificity)
5. 三重激动剂响应预测 (Triple Agonist Response)
6. 个性化建议 (Personalized Recommendations)
7. 科学背景 (Scientific Background)
8. 免责声明 (Disclaimer)

---

## Local Testing

```bash
# Test wild-type
python main.py < test_wildtype.json

# Test variant
python main.py < test_variant.json

# Test heterozygous
python main.py < test_heterozygous.json

# Test missing data
python main.py < test_missing.json
```

---

## Triple Agonist Drugs

| Drug | Status | Company |
|------|--------|---------|
| 瑞他鲁肽 | Phase III | Eli Lilly |
| UBT251 | Clinical | 联邦制药 |
| BGM-0504 | Clinical | 博瑞医药 |

---

## Constraints (WeGene Platform)

| Constraint | Limit |
|------------|-------|
| Execution time | 120 seconds |
| Package size | 10 MB |
| Output size | 1 MB |
| Network access | Not allowed |

---

## Dependencies

None. Uses Python 2.7/3.6 compatible standard library only:
- `sys` - stdin/stderr
- `json` - input parsing

---

## Important Notes

- GCGR Gly40Ser variant is extremely rare in East Asian populations (MAF ~0%)
- Triple agonist drugs are mostly in clinical development
- Report is for reference only, not medical advice

---

## Version

v1.0 - 2024
