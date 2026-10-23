# -*- coding: utf-8 -*-
"""
GLP-1 靶点基因解读逻辑
实现评分算法和风险等级计算
"""

from gene_data import GENES, LOCUS_ORDER, RISK_LEVELS, DRUG_RESPONSE_LEVELS


def sort_genotype(genotype):
    """对基因型进行排序，确保一致性"""
    if genotype is None:
        return None
    return ''.join(sorted(genotype.upper()))


def is_valid_genotype(genotype):
    """检查基因型是否有效"""
    if genotype is None:
        return False
    genotype = genotype.upper()
    return genotype not in ['--', '__', '', 'NA']


def get_genotype_score(gene_key, genotype):
    """
    根据基因型计算评分

    评分规则：
    - 保护基因型: 2分
    - 杂合型: 1分
    - 风险基因型: 0分

    返回: (分数, 基因型类型)
    """
    if not is_valid_genotype(genotype):
        return None, 'unknown'

    gene_info = GENES.get(gene_key)
    if not gene_info:
        return None, 'unknown'

    sorted_gt = sort_genotype(genotype)

    # 检查保护基因型
    protective = [sort_genotype(gt) for gt in gene_info['protective_alleles']]
    if sorted_gt in protective:
        return 2, 'protective'

    # 检查风险基因型
    risk = [sort_genotype(gt) for gt in gene_info['risk_alleles']]
    if sorted_gt in risk:
        return 0, 'risk'

    # 检查杂合型
    hetero = [sort_genotype(gt) for gt in gene_info['heterozygous']]
    if sorted_gt in hetero:
        return 1, 'heterozygous'

    # 未知基因型
    return None, 'unknown'


def calculate_comprehensive_score(genotypes):
    """
    计算综合风险评分

    参数:
        genotypes: dict, {gene_key: genotype}

    返回:
        dict, 包含综合评分、风险等级、各位点评分等
    """
    total_weight = 0
    weighted_score = 0
    locus_scores = {}
    valid_loci = 0

    for gene_key in LOCUS_ORDER:
        gene_info = GENES.get(gene_key)
        if not gene_info:
            continue

        rsid = gene_info['rsid']
        genotype = genotypes.get(gene_key) or genotypes.get(rsid)

        if not is_valid_genotype(genotype):
            locus_scores[gene_key] = {
                'rsid': rsid,
                'genotype': genotype,
                'score': None,
                'type': 'unknown',
                'weight': gene_info['weight'],
                'interpretation': '该位点数据缺失或未检出，无法评估。'
            }
            continue

        score, gt_type = get_genotype_score(gene_key, genotype)
        weight = gene_info['weight']

        if score is not None:
            total_weight += weight
            weighted_score += score * weight
            valid_loci += 1

        # 获取解读文本
        sorted_gt = sort_genotype(genotype)
        interpretation = gene_info['interpretation'].get(sorted_gt, '该基因型的临床意义尚在研究中。')

        locus_scores[gene_key] = {
            'rsid': rsid,
            'genotype': genotype,
            'sorted_genotype': sorted_gt,
            'score': score,
            'type': gt_type,
            'weight': weight,
            'interpretation': interpretation,
            'gene_info': gene_info
        }

    # 计算综合风险百分比（0-100，越高风险越大）
    # 评分越高越保护，所以风险 = 100 - (平均分/2)*100
    if total_weight > 0 and valid_loci > 0:
        avg_score = weighted_score / total_weight
        risk_percentage = 100 - (avg_score / 2) * 100
    else:
        risk_percentage = 50  # 无数据时返回中等风险

    # 确定风险等级
    risk_level = get_risk_level(risk_percentage)

    return {
        'risk_percentage': round(risk_percentage, 1),
        'risk_level': risk_level,
        'locus_scores': locus_scores,
        'valid_loci': valid_loci,
        'total_loci': len(LOCUS_ORDER),
        'avg_score': round(avg_score, 2) if valid_loci > 0 else None
    }


def get_risk_level(percentage):
    """根据风险百分比确定风险等级"""
    for level_key, level_info in RISK_LEVELS.items():
        min_val, max_val = level_info['range']
        if min_val <= percentage < max_val:
            return {
                'key': level_key,
                'name': level_info['name'],
                'description': level_info['description'],
                'color': level_info['color']
            }
    # 默认返回高风险
    return {
        'key': 'high',
        'name': RISK_LEVELS['high']['name'],
        'description': RISK_LEVELS['high']['description'],
        'color': RISK_LEVELS['high']['color']
    }


def assess_drug_response(genotypes):
    """
    评估 GLP-1 受体激动剂药物响应

    主要基于 rs6923761 和 rs3765467 两个药物基因组学位点
    """
    drug_loci = ['GLP1R_rs6923761', 'GLP1R_rs3765467']

    total_score = 0
    valid_count = 0
    weight_sum = 0

    response_details = {}

    for gene_key in drug_loci:
        gene_info = GENES.get(gene_key)
        if not gene_info:
            continue

        rsid = gene_info['rsid']
        genotype = genotypes.get(gene_key) or genotypes.get(rsid)

        if not is_valid_genotype(genotype):
            response_details[gene_key] = {
                'rsid': rsid,
                'status': 'unknown',
                'message': '数据缺失'
            }
            continue

        score, gt_type = get_genotype_score(gene_key, genotype)
        weight = gene_info['weight']

        if score is not None:
            # 对于药物响应，分数越高响应越好
            total_score += score * weight
            weight_sum += weight
            valid_count += 1

        sorted_gt = sort_genotype(genotype)
        response_details[gene_key] = {
            'rsid': rsid,
            'genotype': sorted_gt,
            'score': score,
            'type': gt_type,
            'weight': weight
        }

    # 计算药物响应等级
    if valid_count > 0 and weight_sum > 0:
        avg_response = total_score / weight_sum

        if avg_response >= 1.5:
            response_level = 'good'
        elif avg_response >= 0.5:
            response_level = 'moderate'
        else:
            response_level = 'poor'
    else:
        response_level = 'moderate'  # 数据不足时返回中等

    return {
        'level': response_level,
        'info': DRUG_RESPONSE_LEVELS[response_level],
        'details': response_details,
        'avg_score': round(avg_response, 2) if valid_count > 0 else None
    }


def get_personalized_recommendations(risk_result, drug_response):
    """生成个性化建议"""
    recommendations = []

    risk_level = risk_result['risk_level']['key']
    response_level = drug_response['level']

    # 根据风险等级提供建议
    if risk_level == 'high':
        recommendations.append({
            'category': '监测建议',
            'content': '建议定期进行血糖、糖化血红蛋白检测，密切关注代谢健康指标。'
        })
        recommendations.append({
            'category': '生活方式',
            'content': '建议保持规律运动（每周150分钟中等强度运动），控制饮食中精制碳水化合物摄入。'
        })
    elif risk_level == 'moderate_high':
        recommendations.append({
            'category': '监测建议',
            'content': '建议每年进行血糖检测，关注空腹血糖和餐后血糖变化。'
        })
        recommendations.append({
            'category': '生活方式',
            'content': '建议保持健康体重，适量运动，均衡饮食。'
        })
    else:
        recommendations.append({
            'category': '维持健康',
            'content': '您的基因风险较低，继续保持健康的生活方式即可。'
        })

    # 根据药物响应提供建议
    if response_level == 'good':
        recommendations.append({
            'category': '药物信息',
            'content': '如需使用GLP-1受体激动剂（如司美格鲁肽、利拉鲁肽），预期降糖效果较好。'
        })
    elif response_level == 'moderate':
        recommendations.append({
            'category': '药物信息',
            'content': '如需使用GLP-1受体激动剂，降糖效果可能中等，但体重管理效果可能较好。建议与医生讨论个体化方案。'
        })
    else:
        recommendations.append({
            'category': '药物信息',
            'content': '如需使用GLP-1受体激动剂，降糖效果可能较弱。建议与医生充分沟通，可能需要考虑替代方案或联合用药。'
        })

    return recommendations
