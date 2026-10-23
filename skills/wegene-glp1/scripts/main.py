# -*- coding: utf-8 -*-
"""
GLP-1 靶点基因解读 WeGene 轻应用
主程序入口

功能：
1. 从 stdin 读取 JSON 格式的基因数据
2. 分析 GLP1R 基因多态性
3. 评估代谢风险和药物响应
4. 生成 Markdown 格式报告输出到 stdout
"""

import sys
import json

from gene_data import GENES, LOCUS_ORDER
from interpretation import (
    calculate_comprehensive_score,
    assess_drug_response,
    get_personalized_recommendations
)
from report_generator import generate_report


def get_genotype_from_input(inputs, gene_key):
    """
    从输入数据中获取基因型

    参数:
        inputs: 输入的 JSON 数据中的 inputs 字段
        gene_key: 基因位点的 key (如 'GLP1R_rs10305492')

    返回:
        str 或 None: 基因型字符串
    """
    gene_info = GENES.get(gene_key)
    if not gene_info:
        return None

    rsid = gene_info['rsid']
    genotype = inputs.get(rsid) or inputs.get(gene_key)

    return genotype


def validate_input(inputs):
    """
    验证输入数据是否包含足够的位点

    返回:
        tuple: (bool, str) - (是否有效, 错误信息)
    """
    valid_count = 0
    total_count = len(LOCUS_ORDER)

    for gene_key in LOCUS_ORDER:
        genotype = get_genotype_from_input(inputs, gene_key)
        if genotype and genotype not in ['--', '__', '', 'NA']:
            valid_count += 1

    if valid_count == 0:
        return False, "很抱歉，您的基因数据中缺少 GLP1R 基因的相关位点信息,暂时无法生成解读报告。请确保您的基因检测数据包含 GLP1R 基因位点。"

    return True, None


def process_genetic_data(inputs):
    """
    处理基因数据并生成报告

    参数:
        inputs: 输入的 JSON 数据中的 inputs 字段

    返回:
        str: Markdown 格式的报告
    """
    # 收集所有位点的基因型
    genotypes = {}
    for gene_key in LOCUS_ORDER:
        genotype = get_genotype_from_input(inputs, gene_key)
        if genotype:
            genotypes[gene_key] = genotype

    # 计算综合风险评分
    risk_result = calculate_comprehensive_score(genotypes)

    # 评估药物响应
    drug_response = assess_drug_response(genotypes)

    # 生成个性化建议
    recommendations = get_personalized_recommendations(risk_result, drug_response)

    # 生成完整报告
    report = generate_report(risk_result, drug_response, recommendations, genotypes)

    return report


def main():
    """主程序入口"""
    # 从 stdin 读取输入数据
    body = sys.stdin.read()

    try:
        # 解析 JSON 数据
        data = json.loads(body)
        inputs = data.get('inputs', {})

        # 验证输入数据
        is_valid, error_msg = validate_input(inputs)
        if not is_valid:
            sys.stderr.write(error_msg)
            sys.exit(2)

        # 处理数据并生成报告
        report = process_genetic_data(inputs)

        # 输出报告（只能 print 一次）
        print(report)

    except json.JSONDecodeError as e:
        sys.stderr.write("输入数据格式错误：无法解析 JSON 数据。请检查输入格式是否正确。")
        sys.exit(2)
    except KeyError as e:
        sys.stderr.write("输入数据结构错误：缺少必要的数据字段。")
        sys.exit(2)
    except Exception as e:
        # 输出友好的错误信息
        error_message = "分析过程中遇到错误：{}".format(str(e))
        sys.stderr.write(error_message)
        sys.exit(2)


if __name__ == '__main__':
    main()
