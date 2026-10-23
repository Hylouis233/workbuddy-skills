# -*- coding: utf-8 -*-
"""
Test script for GIP app
"""
import sys
import os
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gene_data import GENES, SCORE_LEVELS, REQUIRED_RSIDS
from interpretation import analyze_genotypes
from report_generator import generate_report
from wegene_utils import is_genotype_exist


def test_with_demo_data():
    """Test with demo data"""
    # Simulate input with all three SNPs detected
    test_input = {
        "inputs": {
            "RS10423928": "AA",
            "RS1800437": "GC",
            "RS11672660": "TT"
        }
    }
    inputs = test_input['inputs']
    print("Testing with input data:")
    for rsid in REQUIRED_RSIDS:
        print("  {}: {}".format(rsid, inputs.get(rsid, 'Not found')))
    print("\nAnalyzing genotypes...")
    results = analyze_genotypes(inputs)
    print("\nAnalysis results:")
    print("  Score:", results['score'])
    print("  Level:", results['level']['title'])
    print("  Available count:", results['available_count'])
    print("\nGenerating report...")
    report = generate_report(results)
    print("\n" + "="*50)
    print("GENERATED REPORT:")
    print("="*50)
    print(report)

if __name__ == "__main__":
    test_with_demo_data()
