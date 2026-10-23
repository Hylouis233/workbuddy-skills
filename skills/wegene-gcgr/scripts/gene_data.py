# -*- coding: utf-8 -*-

# GCGR 受体活性等级定义
RECEPTOR_ACTIVITY_LEVELS = {
    'normal_activity': {
        'name': '正常受体活性',
        'color': 'green',
        'description': '您的GCGR受体功能正常或增强，胰高血糖素信号传导效率高。对以胰高血糖素受体为靶点的激动剂药物响应预期良好。',
        'gcgr_agonist_response': '对胰高血糖素受体激动剂（如玛仕度肽，瑞他鲁肽）响应预期良好，可充分发挥药物增加能量消耗的优势。'
    },
    'mild_reduced_activity': {
        'name': '受体活性轻微降低',
        'color': 'blue',
        'description': '您的GCGR受体功能轻微降低，胰高血糖素信号传导效率略有下降。但整体处于正常范围，对药物响应预期仍然良好。',
        'gcgr_agonist_response': '对胰高血糖素受体激动剂（如玛仕度肽，瑞他鲁肽）响应预期正常，整体影响较小。'
    },
    'reduced_activity': {
        'name': '受体活性降低',
        'color': 'orange',
        'description': '您的GCGR受体功能有所降低，胰高血糖素信号传导效率可能下降。对胰高血糖素受体激动剂药物响应可能受影响。',
        'gcgr_agonist_response': '对胰高血糖素受体激动剂（如玛仕度肽，瑞他鲁肽）的相关效应可能减弱，影响能量消耗的增加。建议与医生讨论个体化治疗方案。'
    }
}

# GCGR 基因位点数据定义
GENES = {
    'GCGR_Gly40Ser': {
        'rsid': 'RS1801483',
        'hgvs_coding': 'NM_000160.5:c.118G>A',
        'hgvs_protein': 'p.Gly40Ser',
        'name': 'GCGR Gly40Ser',
        'gene': 'GCGR',
        'chromosome': '17q25.3',
        'aa_change': 'Gly40Ser (p.G40S)',
        'genotypes': {
            'GG': {
                'level_key': 'normal_activity',
                'category': 'wildtype',
                'description': '野生型纯合子，GCGR受体功能正常。胰高血糖素结合亲和力正常，cAMP信号传导效率标准。'
            },
            'GA': {
                'level_key': 'mild_reduced_activity',
                'category': 'heterozygous',
                'description': '杂合型，携带一个Ser40等位基因。GCGR受体功能轻微降低，胰高血糖素结合亲和力略有下降。'
            },
            'AG': {
                'level_key': 'mild_reduced_activity',
                'category': 'heterozygous',
                'description': '杂合型，携带一个Ser40等位基因。GCGR受体功能轻微降低，胰高血糖素结合亲和力略有下降。'
            },
            'AA': {
                'level_key': 'reduced_activity',
                'category': 'variant',
                'description': '变异纯合型，GCGR受体功能显著降低。功能研究显示该变异可导致胰高血糖素结合亲和力下降约3-4倍。'
            }
        },
        'weight': 1.0,
        'functional_impact': 'Ser40变异位于受体N末端配体结合区域，降低胰高血糖素结合亲和力约3-4倍，减少cAMP信号传导，可能导致轻微的胰高血糖素抵抗表型。',
        'clinical_relevance': '早期研究发现该变异与法国和撒丁岛人群NIDDM相关，但日本和中国研究未发现显著关联。ClinVar分类为良性/可能良性，表明其作为独立致病因素的可能性较低。在胰高血糖素受体激动剂治疗中，该变异可能轻微影响相关药效。',
        'interpretation': {
            'GG': '您的GCGR受体第40位为甘氨酸（野生型），这是最常见的基因型。受体功能正常，对胰高血糖素及以其为靶点的激动剂药物响应预期良好。',
            'GA': '您携带一个Ser40变异等位基因，GCGR受体功能轻微降低。功能研究显示该变异可降低胰高血糖素结合亲和力，但整体影响较小，对药物响应预期仍然良好。',
            'AG': '您携带一个Ser40变异等位基因，GCGR受体功能轻微降低。功能研究显示该变异可降低胰高血糖素结合亲和力，但整体影响较小，对药物响应预期仍然良好。',
            'AA': '您携带两个Ser40变异等位基因，GCGR受体功能降低。该变异在大规模人群数据中被定义为多态性(gnomAD频率0.68%)，对相关药物的响应影响可能较小，但仍建议关注。'
        }
    }
}

# 位点列表（按重要性排序）
LOCUS_ORDER = [
    'GCGR_Gly40Ser',  # 主要功能性位点
]

# 免责声明
DISCLAIMER = """
## 声明

1. 本报告中的受体活性评估基于有限的基因位点，不能完全代表您的整体代谢健康状况
2. 基因只是影响健康的因素之一，生活方式、饮食习惯和环境因素同样重要
3. 药物响应预测仅为参考，实际用药效果因人而异
4. 任何医疗决策应咨询专业医生，请勿自行决定或调整用药方案
5. 本报告不适用于诊断、治疗、治愈或预防任何疾病

"""
