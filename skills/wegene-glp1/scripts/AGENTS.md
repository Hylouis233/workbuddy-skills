<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-03-05 | Updated: 2026-03-21 -->

# glp1-app

## Purpose
GLP-1 (glp1-app) 是一个 WeGene 轻应用，评估 GLP1R 基因多态性以判断代谢风险并预测对 GLP-1 受体激动剂药物的响应。

## Module Overview

GLP-1 (glp1-app) is a WeGene lightweight genetic analysis application that evaluates GLP1R gene polymorphisms to assess metabolic risks and predict response to GLP-1 receptor agonist medications.

**Purpose**: Generate personalized genetic reports for GLP-1 pathway analysis.

**Input**: JSON via stdin containing GLP1R genotypes
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
| `main.py` | Entry point, input validation, orchestration | ~135 |
| `gene_data.py` | GLP1R locus definitions, risk levels, constants | ~175 |
| `interpretation.py` | Scoring algorithm, risk calculation, drug response | ~280 |
| `report_generator.py` | Markdown report generation | ~300 |
| `requirements.txt` | Dependencies (none - stdlib only) | ~4 |
| `README.md` | User documentation | ~60 |

### Test Files

| File | Purpose |
|------|---------|
| `test_input.json` | Standard test case with mixed genotypes |
| `test_high_risk.json` | High-risk genotype test case |
| `test_low_risk.json` | Low-risk genotype test case |
| `test_missing_data.json` | Missing data handling test case |
| `verify_fix.py` | Unit verification script (has syntax errors) |

---

## Core Data Structures

### GENES Dictionary (`gene_data.py`)

6 GLP1R loci with metadata:

```python
GENES = {
    'GLP1R_rs10305492': {  # A316T - cardiovascular protection
        'rsid': 'RS10305492',
        'name': 'GLP-1 A316T',
        'risk_alleles': ['GG'],
        'protective_alleles': ['AA'],
        'heterozygous': ['AG', 'GA'],
        'weight': 1.0,
        'category': 'metabolic_protection',
        'interpretation': {...}
    },
    'GLP1R_rs6923761': {   # G168S - drug response
        'weight': 1.2,
        'category': 'drug_response',
        ...
    },
    'GLP1R_rs3765467': {   # R131Q - drug response
        'weight': 1.2,
        'category': 'drug_response',
        ...
    },
    'GLP1R_rs2268657': {   # T2D risk
        'weight': 0.9,
        'category': 't2d_risk',
        ...
    },
    'GLP1R_rs2268641': {   # Obesity risk
        'weight': 0.7,
        'category': 'obesity_risk',
        ...
    },
    'GLP1R_rs10305420': {  # Receptor function
        'weight': 0.8,
        'category': 'metabolic_protection',
        ...
    }
}
```

### Scoring System (`interpretation.py`)

| Genotype Type | Score |
|---------------|-------|
| Protective | 2 |
| Heterozygous | 1 |
| Risk | 0 |
| Unknown | None |

Risk percentage: `100 - (avg_score / 2) * 100`

### Risk Levels (`gene_data.py`)

| Level | Range | Description |
|-------|-------|-------------|
| Low | 0-30% | Good response expected |
| Moderate-Low | 30-50% | Generally favorable |
| Moderate-High | 50-70% | Monitor recommended |
| High | 70-100% | Intervention recommended |

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
def sort_genotype(genotype) -> str           # Normalize genotype order
def is_valid_genotype(genotype) -> bool      # Check for valid data
def get_genotype_score(gene_key, genotype) -> (int, str)  # (score, type)
def calculate_comprehensive_score(genotypes) -> dict      # Full risk result
def assess_drug_response(genotypes) -> dict               # GLP-1RA response
def get_personalized_recommendations(risk, drug) -> list  # Health advice
```

### report_generator.py

```python
def generate_report(risk_result, drug_response, recommendations, genotypes) -> str
def generate_header() -> str
def generate_gene_overview() -> str
def generate_comprehensive_assessment(risk_result, drug_response) -> str
def generate_detailed_interpretation(locus_scores) -> str
def generate_drug_response_section(drug_response) -> str
def generate_recommendations(recommendations) -> str
def generate_scientific_background() -> str
def generate_disclaimer() -> str
```

---

## Input/Output Format

### Input (stdin JSON)

```json
{
  "inputs": {
    "format": "wegene_affy_2",
    "RS10305492": "AG",
    "RS6923761": "GG",
    "RS3765467": "AG",
    "RS2268641": "CT",
    "RS2268657": "AG",
    "sex": 1,
    "age": 35
  }
}
```

### Output (stdout Markdown)

Structured report with:
1. Header and gene overview
2. Comprehensive risk assessment
3. Detailed locus interpretation
4. Drug response evaluation
5. Personalized recommendations
6. Scientific background
7. Disclaimer

---

## Local Testing

```bash
# Standard test
cat test_input.json | python main.py

# High risk scenario
cat test_high_risk.json | python main.py

# Low risk scenario
cat test_low_risk.json | python main.py
```

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

None. Uses Python 3 standard library only:
- `sys` - stdin/stderr
- `json` - input parsing

---

## Known Issues

1. `verify_fix.py` contains syntax errors (missing commas, incomplete return statement)
2. Output files `n`, `nul`, `output.txt` are artifacts from local testing

---

## Modification Guide

### Adding a New Locus

1. Add entry to `GENES` dictionary in `gene_data.py`
2. Add key to `LOCUS_ORDER` list (position determines display order)
3. Define `risk_alleles`, `protective_alleles`, `heterozygous` arrays
4. Add interpretation text for each genotype
5. Set appropriate `weight` and `category`

### Modifying Risk Calculation

1. Adjust scoring weights in `gene_data.py` (`weight` field)
2. Modify `calculate_comprehensive_score()` in `interpretation.py`
3. Update `RISK_LEVELS` thresholds if needed

### Changing Report Format

1. Edit functions in `report_generator.py`
2. Each section has its own generator function
3. `generate_report()` assembles all sections

---

## Version

v1.0 - Initial release
