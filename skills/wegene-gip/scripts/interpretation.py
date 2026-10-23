# -*- coding: utf-8 -*-
"""
GIPR 基因位点解读逻辑
用于 WeGene 轻应用 - GIP 靶点基因解读
"""

from gene_data import GENES, ORDERED_GENES, SCORE_LEVELS


def sort_genotype(genotype):
    """对基因型进行排序，确保一致性"""
    if genotype and len(genotype) == 2:
        return ''.join(sorted(genotype.upper()))
    return genotype


def is_valid_genotype(genotype):
    """检查基因型是否有效"""
    if not genotype:
        return False
    genotype = genotype.upper()
    return genotype not in ['--', '__', '']


def get_genotype_info(gene_key, genotype):
    """
    获取基因型的详细信息

    Args:
        gene_key: 基因键名（如 'GIPR_rs10423928'）
        genotype: 基因型（如 'AA', 'AT'）

    Returns:
        dict: 基因型信息，包含score, category, description等
    """
    if gene_key not in GENES:
        return None

    gene_info = GENES[gene_key]
    sorted_gt = sort_genotype(genotype)

    if 'genotypes' in gene_info and sorted_gt in gene_info['genotypes']:
        return gene_info['genotypes'][sorted_gt]

    return None


def calculate_score(genotype_results):
    """
    计算综合评分

    Args:
        genotype_results: dict, 每个位点的检测结果

    Returns:
        float: 加权综合评分
    """
    total_score = 0
    total_weight = 0

    for gene_key, result in genotype_results.items():
        if result and result.get('available'):
            score = result.get('score', 0)
            weight = result.get('weight', 1.0)
            total_score += score * weight
            total_weight += weight

    if total_weight > 0:
        return round(total_score / total_weight, 2)
    return 0


def get_score_level(score):
    """
    根据评分获取等级信息

    Args:
        score: float, 综合评分

    Returns:
        dict: 等级信息
    """
    for level_key, level_info in SCORE_LEVELS.items():
        if level_info['min'] <= score <= level_info['max']:
            return level_info
    return SCORE_LEVELS['neutral']


def analyze_genotypes(inputs):
    """
    分析用户基因型

    Args:
        inputs: dict, 从stdin读取的输入数据

    Returns:
        dict: 分析结果
    """
    results = {
        'genotypes': {},
        'available_count': 0,
        'total_count': len(ORDERED_GENES),
        'score': 0,
        'level': None,
        'has_phenotype_separation': False,
        'phenotype_separation_notes': [],
        'ld_info': []
    }

    for gene_key in ORDERED_GENES:
        gene_info = GENES.get(gene_key)
        if not gene_info:
            continue

        rsid = gene_info['rsid']

        genotype_result = {
            'gene_key': gene_key,
            'rsid': rsid,
            'name': gene_info['name'],
            'gene': gene_info['gene'],
            'description': gene_info['description'],
            'genotype': None,
            'score': None,
            'category': None,
            'genotype_description': None,
            'weight': gene_info.get('weight', 1.0),
            'available': False
        }

        # 检查位点是否存在且有效
        if rsid in inputs and is_valid_genotype(inputs[rsid]):
            genotype = sort_genotype(inputs[rsid])
            gt_info = get_genotype_info(gene_key, genotype)

            if gt_info:
                genotype_result['genotype'] = genotype
                genotype_result['score'] = gt_info['score']
                genotype_result['category'] = gt_info['category']
                genotype_result['genotype_description'] = gt_info['description']
                genotype_result['available'] = True
                results['available_count'] += 1

        results['genotypes'][gene_key] = genotype_result

        # 检查表型分离现象
        if gene_info.get('phenotype_separation') and genotype_result['available']:
            results['has_phenotype_separation'] = True
            results['phenotype_separation_notes'] = gene_info.get('phenotype_notes', [])

        # 收集连锁信息
        if gene_info.get('ld_with') and genotype_result['available']:
            results['ld_info'].append({
                'rsid': rsid,
                'ld_with': gene_info['ld_with'],
                'notes': gene_info.get('ld_notes', '')
            })

    # 计算综合评分
    results['score'] = calculate_score(results['genotypes'])
    results['level'] = get_score_level(results['score'])

    return results


def get_phenotype_separation_message(results):
    """
    生成表型分离现象的解读信息

    Args:
        results: dict, analyze_genotypes的结果

    Returns:
        str: 表型分离解读信息
    """
    if not results.get('has_phenotype_separation'):
        return None

    gt_result = results['genotypes'].get('GIPR_rs10423928')
    if not gt_result or not gt_result['available']:
        return None

    genotype = gt_result['genotype']
    notes = results.get('phenotype_separation_notes', [])

    message = "## 表型分离现象说明\n\n"
    message += "rs10423928位点展示了一种非常经典的**表型分离**效应：\n\n"

    if genotype == 'AA':
        message += "您携带的AA基因型与以下特征相关：\n"
    elif genotype in ['AT', 'TA']:
        message += "您携带的杂合型可能展示部分表型分离效应：\n"
    else:
        message += "您携带的TT基因型为野生型：\n"

    for note in notes:
        message += f"- {note}\n"

    message += "\n> 这种独特的遗传效应使得rs10423928成为评估GIP通路功能的重要遗传标记。"

    return message


def get_tirzepatide_prediction(results):
    """
    生成替泊泽肽响应预测信息

    Args:
        results: dict, analyze_genotypes的结果

    Returns:
        str: 替泊泽肽响应预测
    """
    level = results.get('level')
    if not level:
        return "基于您的基因型，无法提供明确的药物响应预测。"

    score = results['score']

    prediction = f"**综合评分**: {score}/2\n\n"
    prediction += f"**预测响应**: {level['tirzepatide_response']}\n\n"

    gt_10423928 = results['genotypes'].get('GIPR_rs10423928', {})
    if gt_10423928.get('available') and gt_10423928.get('genotype') == 'AA':
        prediction += "**特殊说明**:\n"
        prediction += "由于您携带rs10423928 AA基因型，GIP通路可能对替泊泽肽的GIPR激动作用更为敏感。"

    return prediction
