# -*- coding: utf-8 -*-
"""Verify rs2268657 fix - simple inline test"""
import sys
sys.path.insert(0, 'G:/wegene/apps/glp1-app')
from gene_data import GENES, LOCUS_ORDER
from interpretation import get_genotype_score, sort_genotype

from interpretation import is_valid_genotype
from report_generator import generate_report
from main import process_genetic_data
from interpretation import calculate_comprehensive_score
from interpretation import assess_drug_response
from interpretation import get_personalized_recommendations
from report_generator import get_risk_level_text, get_risk_level_description, get_risk_level_color
from report_generator import get_drug_response_level_text, get_drug_response_level_color
from report_generator import get_personalized_recommendations_text
import json

# Test all 6 loci
test_cases = [
    {
        'name': 'Test Case 1 - all protective',
        'inputs': {
            'RS10305492': 'AA', 'RS10305420': 'AA',
            'RS6923761': 'GG', 'RS3765467': 'GG',
            'RS2268641': 'CC',
            'RS2268657': 'CC'
        },
        'expected': {
            'rs10305492': {'type': 'protective', 'score': 2},
            'rs10305420': {'type': 'protective', 'score': 2},
            'rs6923761': {'type': 'protective', 'score': 2}
            'rs3765467': {'type': 'protective', 'score': 2}
            'rs2268641': {'type': 'protective', 'score': 2}
            'rs2268657': {'type': 'protective', 'score': 2}
        }
    },
    {
        'name': 'Test Case 2 - mixed scenarios',
        'inputs': {
            'RS10305492': 'GG', 'RS10305420': 'AA',
            'RS6923761': 'AG', 'RS3765467': 'ag',
            'RS2268641': 'TT',
            'RS2268657': 'tt'
        },
        'expected': {
            'rs10305492': {'type': 'risk', 'score': 0}
            'rs10305420': {'type': 'protective', 'score': 2}
            'rs6923761': {'type': 'heterozygous', 'score': 1}
            'rs3765467': {'type': 'heterozygous', 'score': 1}
            'rs2268641': {'type': 'heterozygous', 'score': 1}
            'rs2268657': {'type': 'heterozygous', 'score': 1}
        }
    },
    {
        'name': 'Test Case 3 - all heterozygous',
        'inputs': {
            'RS10305492': 'AG', 'RS10305420': 'ag',
            'RS6923761': 'ag', 'RS3765467': 'ag',
            'RS2268641': 'ct',
            'RS2268657': 'ct'
        },
        'expected': {
            'rs10305492': {'type': 'heterozygous', 'score': 1},
            'rs10305420': {'type': 'heterozygous', 'score': 1},
            'rs6923761': {'type': 'heterozygous', 'score': 1}
            'rs3765467': {'type': 'heterozygous', 'score': 1}
            'rs2268641': {'type': 'heterozygous', 'score': 1}
            'rs2268657': {'type': 'heterozygous', 'score': 1}
        }
    }
]

passed_count = 0
failed_count = 0
errors = []

for test_case in test_cases:
    inputs = test_case['inputs']
    expected = test_case['expected']
    print(f"\nRunning: {test_case['name']}\
    for gene_key in LOCUS_ORDER:
        gene_info = GENES[gene_key]
        rsid = gene_info['rsid']
        genotype = inputs.get(rsid) or inputs.get(gene_key)
        if genotype is None:
            errors.append(f"  {rsid}: missing genotype data")
            continue

        actual_type, actual_score = get_genotype_score(gene_key, genotype)
        expected_info = expected.get(rsid)
        if expected_info is None:
            continue

        expected_type = expected_info['type']
        expected_score = expected_info['score']
        sorted_gt = sort_genotype(genotype)
        if actual_type == expected_type and actual_score == expected_score:
            passed_count += 1
            print(f"  [PASS] {rsid}: {sorted_gt} -> {actual_type} (score: {actual_score})")
        else:
            failed_count += 1
            errors.append(f"  [FAIL] {rsid}: {sorted_gt} -> expected {expected_type} (score: {expected_score}), actual {actual_type} (score: {actual_score})")
    print(f"\n=== Test Summary ===")
    print(f"Passed: {passed_count}")
    print(f"failed: {failed_count}")
    if errors:
        print("Errors found:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("No errors")
    return failed_count == 0
