# -*- coding: utf-8 -*-
"""
GIPR 基因位点数据定义
用于 WeGene 轻应用 - GIP 靶点基因解读
"""

# 需要申请的位点列表
REQUIRED_RSIDS = ['RS10423928', 'RS1800437', 'RS11672660']

# 评分等级定义
SCORE_LEVELS = {
    'high_protection': {
        'min': 4,
        'max': 6,
        'title': '高度保护型',
        'description': '您的基因型携带多个GIPR功能缺失变异。研究表明，GIPR功能缺失与显著降低的肥胖风险、更低的BMI以及改善的代谢健康指标相关。',
        'tirzepatide_response': '研究数据提示，此类基因型携带者在使用替泊泽肽（Tirzepatide）等双靶点药物时，可能获得比平均水平更显著的体重减轻效果。'
    },
    'moderate_protection': {
        'min': 2,
        'max': 3.9,
        'title': '中度保护型',
        'description': '您的基因型携带部分GIPR保护性变异。相比普通人群，您可能具有较低的BMI和肥胖风险，代谢灵活性较好。',
        'tirzepatide_response': '预计对替泊泽肽（Tirzepatide）有良好的响应，减重获益可能优于人群平均水平。'
    },
    'neutral': {
        'min': 0.5,
        'max': 1.9,
        'title': '中性型',
        'description': '您的基因型显示GIPR受体功能处于基线水平。这意味着您的肥胖风险和代谢特征与普通人群相当，主要受生活方式影响。',
        'tirzepatide_response': '预计对替泊泽肽（Tirzepatide）表现为标准响应，疗效符合临床试验的平均预期。'
    },
    'risk': {
        'min': 0,
        'max': 0.4,
        'title': '标准型',
        'description': '您的基因型未携带GIPR保护性变异，GIPR受体功能完整。相比保护型人群，您在维持健康体重方面可能面临常规挑战，需要更注意饮食和运动平衡。',
        'tirzepatide_response': '预计对替泊泽肽（Tirzepatide）表现为标准响应。建议严格配合饮食控制和规律运动以获得最佳药物效果。'
    }
}

# GIPR 基因位点定义
GENES = {
    'GIPR_rs10423928': {
        'rsid': 'RS10423928',
        'name': 'GIP受体核心位点',
        'gene': 'GIPR',
        'description': 'GIPR基因关键内含子变异，影响受体功能和代谢特征',
        'genotypes': {
            'AA': {'score': 2, 'category': 'protective', 'description': '双侧保护型。携带两个功能缺失等位基因，与较低的BMI和显著降低的肥胖风险相关。在使用GIPR相关药物时可能更敏感。'},
            'AT': {'score': 1, 'category': 'heterozygous', 'description': '杂合型。携带一个保护性等位基因，与轻度降低的BMI和肥胖风险相关。GIPR受体功能部分受损，提供一定的代谢保护。'},
            'TA': {'score': 1, 'category': 'heterozygous', 'description': '杂合型。携带一个保护性等位基因，与轻度降低的BMI和肥胖风险相关。GIPR受体功能部分受损，提供一定的代谢保护。'},
            'TT': {'score': 0, 'category': 'wildtype', 'description': '野生型纯合子。GIPR受体功能完整活跃，未携带保护性变异。代谢特征处于人群基线水平，无额外的遗传保护效应。'}
        },
        'weight': 1.5,
        'phenotype_separation': True,
        'phenotype_notes': [
            'BMI: 保护性等位基因(A)与更低的BMI和腰围显著相关',
            '胰岛素: A等位基因可能导致GIP刺激的胰岛素分泌减少，但整体代谢更健康',
            '药物: A等位基因携带者对替泊泽肽的减重响应可能更佳'
        ]
    },
    'GIPR_rs1800437': {
        'rsid': 'RS1800437',
        'name': 'GIPR E354Q错义突变',
        'gene': 'GIPR',
        'description': 'GIPR基因错义突变(E354Q)，影响受体结构',
        'genotypes': {
            'CC': {'score': 2, 'category': 'protective', 'description': '双侧保护型。通常与rs10423928-AA连锁，共同导致GIPR功能降低，从而降低肥胖风险。'},
            'CG': {'score': 1, 'category': 'heterozygous', 'description': '杂合型。携带一个变异拷贝，通常与rs10423928-AT连锁，提供部分代谢保护效应。'},
            'GC': {'score': 1, 'category': 'heterozygous', 'description': '杂合型。携带一个变异拷贝，通常与rs10423928-AT连锁，提供部分代谢保护效应。'},
            'GG': {'score': 0, 'category': 'wildtype', 'description': '野生型纯合子。受体结构未发生该特定变异，功能正常。未携带相关的肥胖保护因素。'}
        },
        'weight': 1.2,
        'ld_with': 'RS10423928',
        'ld_notes': '该位点与rs10423928存在高度连锁不平衡，解读参考核心位点'
    },
    'GIPR_rs11672660': {
        'rsid': 'RS11672660',
        'name': 'GIPR代谢综合征相关位点',
        'gene': 'GIPR',
        'description': '与代谢综合征风险相关的GIPR基因多态性',
        'genotypes': {
            'TT': {'score': 2, 'category': 'protective', 'description': '保护型。研究表明该基因型可能与较低的空腹血糖和血脂水平相关，有助于降低代谢综合征风险。'},
            'CT': {'score': 0, 'category': 'risk', 'description': '风险型。携带风险等位基因，研究发现在代谢综合征人群中频率较高，建议定期监测血脂血糖。'},
            'TC': {'score': 0, 'category': 'risk', 'description': '风险型。携带风险等位基因，研究发现在代谢综合征人群中频率较高，建议定期监测血脂血糖。'},
            'CC': {'score': 1, 'category': 'neutral', 'description': '中性型。该位点对代谢综合征风险的影响处于平均水平，建议保持健康饮食习惯。'}
        },
        'weight': 1.0
    }
}

# 位点列表（按重要性排序）
ORDERED_GENES = ['GIPR_rs10423928', 'GIPR_rs1800437', 'GIPR_rs11672660']

# 科学背景信息
SCIENCE_BACKGROUND = """
## GIPR基因与肠促胰素系统

GIPR（葡萄糖依赖性胰岛素促泌多肽受体）是肠促胰素系统的核心受体之一。

### 生理功能
- **胰岛素分泌调节**: 介导GIP激素的葡萄糖依赖性胰岛素促泌作用
- **β细胞保护**: 促进胰岛β细胞增殖，抑制凋亡
- **脂肪代谢**: 调节脂肪细胞的生长和分化

### 替泊泽肽(Tirzepatide)
替泊泽肽是首个获批的双重GIPR/GLP-1R激动剂，对两个通路同时起作用。

### 参考文献
- Nature Metabolism (2024): GIPR变异功能研究
- PMID: 25047836: GIPR变异与T2D患者卒中风险
Characterization of genetic variants of GIPR reveals a contribution of β-arrestin to metabolic phenotypes https://www.nature.com/articles/s42255-024-01061-4
A naturally occurring GIP receptor variant undergoes enhanced agonist-induced desensitization, which impairs GIP control of adipose insulin sensitivity https://pubmed.ncbi.nlm.nih.gov/25047836/
"""

# 免责声明
DISCLAIMER = """
---
## 免责声明

本报告仅基于有限的基因位点信息提供参考性解读，不能作为医学诊断或治疗依据。

1. **局限性**: 基因检测仅反映遗传倾向，实际健康状况受多种因素影响
2. **非诊断**: 本报告不构成任何疾病的诊断或预测
3. **咨询建议**: 如有健康疑虑，请咨询专业医疗人员
4. **药物使用**: 任何药物的使用必须在医生指导下进行

**本解读由WeGene轻应用自动生成，仅供参考。**
"""
