# -*- coding: utf-8 -*-
"""
GCGR 靶点基因解读逻辑
实现受体活性评分算法和胰高血糖素受体激动剂响应预测
"""

from gene_data import (
    GENES, LOCUS_ORDER, RECEPTOR_ACTIVITY_LEVELS
)


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


def get_genotype_info(gene_key, genotype):
    """
    获取基因型详细信息

    返回: dict 包含评分、分类、描述等
    """
    if not is_valid_genotype(genotype):
        return None

    gene_info = GENES.get(gene_key)
    if not gene_info:
        return None

    sorted_gt = sort_genotype(genotype)
    genotypes_info = gene_info.get('genotypes', {})

    if sorted_gt in genotypes_info:
        gt_info = genotypes_info[sorted_gt].copy()
        gt_info['sorted_genotype'] = sorted_gt
        gt_info['original_genotype'] = genotype
        gt_info['gene_info'] = gene_info
        return gt_info

    return None


def get_activity_level(genotype_results):
    """
    根据主位点的基因型直接获取受体活性等级

    参数:
        genotype_results: 基因型分析结果字典

    返回:
        dict 活性等级信息
    """
    # 获取主要功能性位点（由于当前只有一个位点，直接取第一个）
    main_locus = LOCUS_ORDER[0]
    result = genotype_results.get(main_locus)

    if not result:
        return {
            'key': 'unknown',
            'name': '未知',
            'description': '无法评估受体活性，未能取得数据。',
            'color': 'gray',
            'gcgr_agonist_response': '无法预测药物响应。'
        }

    level_key = result.get('level_key', 'normal_activity')
    level_info = RECEPTOR_ACTIVITY_LEVELS.get(level_key, RECEPTOR_ACTIVITY_LEVELS['normal_activity'])

    return {
        'key': level_key,
        'name': level_info['name'],
        'description': level_info['description'],
        'color': level_info['color'],
        'gcgr_agonist_response': level_info['gcgr_agonist_response']
    }


def get_gcgr_agonist_prediction(results):
    """
    获取胰高血糖素受体激动剂响应预测

    参数:
        results: 完整分析结果

    返回:
        dict 药物响应预测信息
    """
    activity_level = results.get('activity_level', {})
    activity_key = activity_level.get('key')

    prediction = {
        'overall_response': activity_level.get('gcgr_agonist_response', '无法预测'),
        'gcgr_contribution': '正常' if activity_key == 'normal_activity' else ('轻微降低' if activity_key == 'mild_reduced_activity' else '显著降低'),
        'drug_recommendations': []
    }

    # 根据活性等级提供药物建议
    if activity_key == 'normal_activity':
        prediction['drug_recommendations'].append({
            'drug': '玛仕度肽 (Mazdutide)',
            'suitability': '高度契合',
            'note': '您的GCGR受体功能正常，预期能充分发挥该类药物在增加能量消耗、促进脂肪氧化方面的核心优势，从而达到强效减重目的。'
        })
    elif activity_key == 'mild_reduced_activity':
        prediction['drug_recommendations'].append({
            'drug': '玛仕度肽 (Mazdutide)',
            'suitability': '适合',
            'note': '您的GCGR受体功能虽有轻微波动，但整体处于正常范围，仍可较好地响应此类以胰高血糖素受体激动为核心的减重药物。'
        })
    else:
        prediction['drug_recommendations'].append({
            'drug': '玛仕度肽 (Mazdutide)',
            'suitability': '需个体化评估',
            'note': '您的GCGR受体功能可能偏低，可能导致该类药物通过激活胰高血糖素受体来增加能量消耗的效率打折，建议加强运动。'
        })

    return prediction


def check_population_warning(genotype_results):
    """
    检查是否需要人群特异性警告

    东亚人群中Gly40Ser变异极罕见，检测到变异时需要特别提示

    返回:
        dict 人群警告信息
    """
    warning = {
        'show_warning': False,
        'message': '',
        'details': ''
    }

    for gene_key, result in genotype_results.items():
        if result is None:
            continue

        gene_info = result.get('gene_info', {})
        genotype = result.get('sorted_genotype', '')

        # 检查是否携带变异等位基因
        if 'A' in genotype and genotype != 'GG':
            warning['show_warning'] = True
            warning['message'] = '您携带的GCGR Gly40Ser变异在东亚人群中较为罕见'
            warning['details'] = (
                'GCGR Gly40Ser (RS1801483) 变异在欧洲人群中的携带频率约为2-8%，'
                '建议结合家族史和祖源信息综合解读。此变异可能轻微影响GCGR受体功能，'
                '进而影响对胰高血糖素受体激动剂类药物的响应。'
            )
            break

    return warning


def analyze_genotypes(inputs):
    """
    核心分析函数：分析GCGR基因型

    参数:
        inputs: 用户输入数据（包含基因型信息）

    返回:
        dict 完整分析结果
    """
    genotype_results = {}
    available_count = 0

    for gene_key in LOCUS_ORDER:
        gene_info = GENES.get(gene_key, {})
        rsid = gene_info.get('rsid', '')

        # 尝试多种方式获取基因型
        genotype = inputs.get(rsid) or inputs.get(gene_key) or inputs.get(rsid.lower())

        if is_valid_genotype(genotype):
            gt_info = get_genotype_info(gene_key, genotype)
            genotype_results[gene_key] = gt_info
            available_count += 1
        else:
            genotype_results[gene_key] = None

    # 获取活性等级
    activity_level = get_activity_level(genotype_results)

    # 构建结果
    results = {
        'genotypes': genotype_results,
        'available_count': available_count,
        'total_count': len(LOCUS_ORDER),
        'activity_level': activity_level,
    }

    # 胰高血糖素受体激动剂响应预测
    results['gcgr_agonist_prediction'] = get_gcgr_agonist_prediction(results)

    # 人群特异性警告
    results['population_warning'] = check_population_warning(genotype_results)

    return results


def get_personalized_recommendations(results):
    """
    生成个性化建议

    参数:
        results: 分析结果

    返回:
        list 建议列表
    """
    recommendations = []

    activity_key = results['activity_level'].get('key', 'normal_activity')
    population_warning = results.get('population_warning', {})

    # 根据受体活性提供建议
    if activity_key == 'normal_activity':
        recommendations.append({
            'category': '受体功能',
            'content': '您的GCGR受体功能正常或更优，胰高血糖素信号传导效率良好。'
        })
        recommendations.append({
            'category': '药物响应',
            'content': '如考虑使用以胰高血糖素受体为核心靶点的减重药物（如玛仕度肽，瑞他鲁肽），预期可获得显著的能量消耗提升和减重效果。'
        })
    elif activity_key == 'mild_reduced_activity':
        recommendations.append({
            'category': '受体功能',
            'content': '您的GCGR受体功能虽有轻微下降，但整体处于正常范围，胰高血糖素信号传导基本正常。'
        })
        recommendations.append({
            'category': '药物响应',
            'content': '对以胰高血糖素受体为核心靶点的减重药物响应预期良好，仍可作为减重方案的有效选择。'
        })
    else:
        recommendations.append({
            'category': '受体功能',
            'content': '您的GCGR受体功能有所降低，可能影响胰高血糖素信号传导效率。'
        })
        recommendations.append({
            'category': '药物响应',
            'content': '由于靶点受体活性受限，使用以胰高血糖素受体激动为核心机制的药物时，增加能量消耗的获益可能有所减弱，建议在医生指导下选择最适合的减重手段。'
        })

    # 人群特异性建议
    if population_warning.get('show_warning'):
        recommendations.append({
            'category': '人群特异性',
            'content': '您携带的GCGR变异在东亚人群中极罕见，建议结合家族史和祖源信息综合解读结果。'
        })

    # 通用代谢健康建议
    recommendations.append({
        'category': '代谢健康',
        'content': '科学减重不仅依赖药物，保持健康的生活方式（如均衡饮食、规律有氧与力量训练相结合）对于打破减重平台期至关重要。'
    })

    recommendations.append({
        'category': '定期监测',
        'content': '在减重期间，建议定期监测体重、体脂率以及血糖、血脂等核心代谢指标，评估方案的有效性。'
    })

    return recommendations
