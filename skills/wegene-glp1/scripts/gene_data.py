# -*- coding: utf-8 -*-
"""
GLP-1 靶点基因数据定义
定义 GLP1R 基因上与 GLP-1 药物响应和代谢健康相关的核心位点
"""

# GLP1R 基因位点数据定义
# 每个位点包含：rs号、名称、风险/保护基因型、权重、描述等信息
GENES = {
    'GLP1R_rs10305492': {
        'rsid': 'RS10305492',
        'name': 'GLP-1受体 A316T',
        'gene': 'GLP1R',
        'aa_change': 'Ala316Thr',
        'risk_alleles': ['GG'],  # 野生型 - 正常风险
        'protective_alleles': ['AA'],  # A等位基因纯合 - 心血管和代谢保护
        'heterozygous': ['AG', 'GA'],  # 杂合型 - 部分保护
        'weight': 1.0,
        'maf': 0.014,  # 东亚人群约1.4%
        'category': 'metabolic_protection',
        'description': 'GLP1R基因上著名的低频错义突变，携带A等位基因(Thr316)具有显著的心脏和代谢保护作用，能降低空腹血糖、2型糖尿病及心血管疾病风险。',
        'interpretation': {
            'GG': '您的GLP-1受体在第316位为丙氨酸（野生型），这是最常见的基因型，代谢风险处于平均水平。',
            'AG': '您携带一个A等位基因（Thr316），具有部分心血管和代谢保护作用，空腹血糖水平可能较低。',
            'AA': '您携带两个A等位基因（Thr316纯合），具有显著的心血管和代谢保护作用，但该基因型在人群中较为罕见。'
        }
    },
    'GLP1R_rs10305420': {
        'rsid': 'RS10305420',
        'name': 'GLP-1受体 Pro7Leu/Arg',
        'gene': 'GLP1R',
        'aa_change': 'Pro7Leu/Arg',
        'risk_alleles': ['CC'],  # 野生型
        'protective_alleles': ['TT'],  # 保护型
        'heterozygous': ['CT', 'TC'],
        'weight': 0.8,
        'maf': 0.15,  # 东亚人群约15%
        'category': 'metabolic_protection',
        'description': 'GLP1R基因N末端的错义突变，可能影响受体与配体的结合能力。',
        'interpretation': {
            'CC': '您的GLP-1受体N末端为野生型，受体功能处于正常水平。',
            'CT': '您携带一个变异等位基因，受体功能可能有轻微改变。',
            'TT': '您携带两个变异等位基因，受体功能可能有中度改变。'
        }
    },
    'GLP1R_rs6923761': {
        'rsid': 'RS6923761',
        'name': 'GLP-1受体 Gly168Ser',
        'gene': 'GLP1R',
        'aa_change': 'Gly168Ser',
        'risk_alleles': ['AA'],  # A等位基因 - 药物响应较差
        'protective_alleles': ['GG'],  # G等位基因 - 药物响应较好
        'heterozygous': ['AG', 'GA'],
        'weight': 1.2,  # 药物基因组学权重较高
        'maf': 0.30,  # 约30%人群携带A等位基因
        'category': 'drug_response',
        'description': 'GLP1R基因最常见的功能性多态性之一，与GLP-1受体激动剂（如司美格鲁肽、利拉鲁肽）的降糖疗效直接相关。野生型GG对药物响应更好，但A等位基因携带者在体重减轻方面效果可能更好。',
        'interpretation': {
            'GG': '您对GLP-1受体激动剂的降糖响应可能较好，糖化血红蛋白改善程度通常更显著。标准剂量治疗预期效果良好。',
            'AG': '您对GLP-1受体激动剂的降糖响应可能中等，但体重减轻效果可能更好。可根据实际情况调整治疗方案。',
            'AA': '您对GLP-1受体激动剂的降糖响应可能较弱，但在体重管理方面可能有更好效果。建议与医生讨论个体化治疗方案。'
        }
    },
    'GLP1R_rs3765467': {
        'rsid': 'RS3765467',
        'name': 'GLP-1受体 Arg131Gln',
        'gene': 'GLP1R',
        'aa_change': 'Arg131Gln',
        'risk_alleles': ['AA'],  # A等位基因 - 药物响应较差
        'protective_alleles': ['GG'],  # G等位基因 - 药物响应较好
        'heterozygous': ['AG', 'GA'],
        'weight': 1.2,  # 药物基因组学权重较高
        'maf': 0.25,  # 东亚人群约25%
        'category': 'drug_response',
        'description': 'GLP1R基因上影响药物响应的错义突变，显著影响患者对GLP-1受体激动剂的治疗响应。野生型GG患者HbA1c下降幅度更大（约1.7% vs 0.8%）。',
        'interpretation': {
            'GG': '您对GLP-1受体激动剂的降糖响应可能较好，HbA1c达标率约50.9%，治疗效果预期良好。',
            'AG': '您对GLP-1受体激动剂的降糖响应可能中等，建议监测治疗效果并根据需要调整方案。',
            'AA': '您对GLP-1受体激动剂的降糖响应可能较弱，HbA1c下降幅度可能较小。建议与医生讨论替代方案或联合用药。'
        }
    },
    'GLP1R_rs2268641': {
        'rsid': 'RS2268641',
        'name': 'GLP-1受体肥胖相关位点',
        'gene': 'GLP1R',
        'aa_change': None,  # 内含子变异
        'risk_alleles': ['CC'],  # C等位基因 - 肥胖风险较高
        'protective_alleles': ['TT'],  # T等位基因 - 肥胖保护
        'heterozygous': ['CT', 'TC'],
        'weight': 0.7,
        'maf': 0.38,  # 约38%
        'category': 'obesity_risk',
        'description': 'GLP1R基因上的多态性位点，主要与肥胖风险相关。TT基因型可能对超重具有保护作用（OR=0.66）。',
        'interpretation': {
            'CC': '您的基因型与正常肥胖风险相关，建议保持健康的生活方式。',
            'CT': '您携带一个保护等位基因，超重风险可能略有降低。',
            'TT': '您的基因型可能对超重具有保护作用，但仍需保持健康的生活方式。'
        }
    },
    'GLP1R_rs2268657': {
        'rsid': 'RS2268657',
        'name': 'GLP-1受体糖尿病风险位点',
        'gene': 'GLP1R',
        'aa_change': None,
        'risk_alleles': ['CC'],  # C等位基因 - T2D风险较高
        'protective_alleles': ['TT'],  # T等位基因 - 保护
        'heterozygous': ['CT', 'TC'],
        'weight': 0.9,
        'maf': 0.32,  # 约32%
        'category': 't2d_risk',
        'description': 'GLP1R基因上与2型糖尿病风险相关的多态性位点，CC基因型与T2DM发生显著相关（OR约3.2）。',
        'interpretation': {
            'CC': '您的基因型与较高的2型糖尿病风险相关（OR约3.2），建议定期监测血糖并保持健康生活方式。',
            'CT': '您携带一个保护等位基因，2型糖尿病风险可能处于中等水平。',
            'TT': '您的基因型与较低的2型糖尿病风险相关，但仍需保持健康的生活方式。'
        }
    }
}

# 位点列表（按重要性排序）
LOCUS_ORDER = [
    'GLP1R_rs10305492',  # 心血管代谢保护
    'GLP1R_rs6923761',   # 药物响应
    'GLP1R_rs3765467',   # 药物响应
    'GLP1R_rs2268657',   # T2D风险
    'GLP1R_rs2268641',   # 肥胖风险
    'GLP1R_rs10305420',  # 其他功能位点
]

# 风险等级定义
RISK_LEVELS = {
    'low': {
        'name': '低风险',
        'range': (0, 30),
        'color': 'green',
        'description': '您的基因特征显示对GLP-1通路相关代谢风险较低，对GLP-1受体激动剂可能有较好的治疗响应。'
    },
    'moderate_low': {
        'name': '中低风险',
        'range': (30, 50),
        'color': 'blue',
        'description': '您的基因特征显示对GLP-1通路相关代谢风险处于中低水平，总体情况良好。'
    },
    'moderate_high': {
        'name': '中高风险',
        'range': (50, 70),
        'color': 'orange',
        'description': '您的基因特征显示对GLP-1通路相关代谢风险处于中高水平，建议关注血糖监测和生活方式干预。'
    },
    'high': {
        'name': '高风险',
        'range': (70, 100),
        'color': 'red',
        'description': '您的基因特征显示对GLP-1通路相关代谢风险较高，建议与医生讨论个体化的预防和治疗方案。'
    }
}

# 药物响应等级定义
DRUG_RESPONSE_LEVELS = {
    'good': {
        'name': '响应良好',
        'description': '基于您的基因型，预期对GLP-1受体激动剂的降糖效果较好。'
    },
    'moderate': {
        'name': '响应中等',
        'description': '基于您的基因型，对GLP-1受体激动剂的降糖效果可能中等，但体重管理效果可能较好。'
    },
    'poor': {
        'name': '响应较弱',
        'description': '基于您的基因型，对GLP-1受体激动剂的降糖效果可能较弱，建议与医生讨论个体化治疗方案。'
    }
}
