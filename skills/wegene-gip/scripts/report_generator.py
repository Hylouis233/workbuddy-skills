# -*- coding: utf-8 -*-
"""
GIPR 基因报告生成器
用于 WeGene 轻应用 - GIP 靶点基因解读
"""

from gene_data import DISCLAIMER


def generate_report(results):
    """
    生成完整的Markdown格式报告

    Args:
        results: dict, analyze_genotypes的返回结果

    Returns:
        str: Markdown格式的完整报告
    """
    report_parts = []

    # 标题
    report_parts.append("# GIPR 靶点基因解读报告")

    # 综合评估
    report_parts.append(generate_overall_assessment(results))

    # 详细位点解读
    report_parts.append(generate_detailed_interpretation(results))

    # 表型分离说明（如果适用）
    if results.get('has_phenotype_separation'):
        report_parts.append(generate_phenotype_separation_section(results))

    # 个性化建议
    report_parts.append(generate_personalized_recommendations(results))

    # 免责声明
    report_parts.append(DISCLAIMER)

    return '\n'.join(report_parts)


def generate_overall_assessment(results):
    """生成综合评估部分"""
    level = results['level']
    score = results['score']

    assessment = f"""
## 综合评估

### 评分结果

| 指标 | 结果 |
|------|------|
| **综合评分** | {score}/2 |
| **分类** | {level['title']} |
| **描述** | {level['description']} |

### 替泊泽肽(Tirzepatide)响应预测

{level['tirzepatide_response']}
"""
    return assessment


def generate_detailed_interpretation(results):
    """生成详细位点解读部分"""
    details = """
## 详细位点解读

"""
    for gene_key in results['genotypes']:
        gt_info = results['genotypes'][gene_key]

        details += f"### {gt_info['rsid']} - {gt_info['name']}\n\n"
        details += f"**基因**: {gt_info['gene']}\n\n"
        details += f"**功能描述**: {gt_info['description']}\n\n"

        if gt_info['available']:
            details += f"**您的基因型**: `{gt_info['genotype']}`\n\n"

            # 基因型分类标签
            category_label = {
                'protective': '保护型',
                'risk': '风险型',
                'heterozygous': '杂合型',
                'neutral': '中性型',
                'wildtype': '野生型'
            }
            cat_text = category_label.get(gt_info['category'], gt_info['category'])
            details += f"**分类**: {cat_text}\n\n"
            details += f"**解读**: {gt_info['genotype_description']}\n\n"
        else:
            details += "**您的基因型**: 未检测或数据缺失\n\n"
            details += "**解读**: 该位点数据不可用，无法提供解读\n\n"

        details += "---\n\n"

    return details


def generate_phenotype_separation_section(results):
    """生成表型分离现象说明部分"""
    phenotype_notes = results.get('phenotype_separation_notes', [])

    section = """
## 表型分离现象说明

rs10423928位点展示了一种非常经典的**"表型分离"**效应，即同一基因变异对不同生理指标产生相反的影响。

### 对您的意义

"""
    for note in phenotype_notes:
        section += f"- {note}\n"

    return section


def generate_personalized_recommendations(results):
    """生成个性化建议部分"""
    level = results['level']
    score = results['score']
    gt_10423928 = results['genotypes'].get('GIPR_rs10423928', {})

    recommendations = """
## 个性化建议

### 代谢健康管理

"""
    if score >= 2:
        recommendations += """
- **天然遗传优势**：您的基因型携带GIPR功能缺失变异，研究表明这与较低的BMI和显著降低的肥胖风险相关。
- **健康维护**：虽然您具有遗传保护，但不良的生活方式仍可能抵消这种优势。建议保持规律运动以维持肌肉量，因为GIPR功能缺失可能会影响脂肪分布。
- **监测建议**：您的空腹血糖可能略高（这是该保护型变异的已知特征），但通常在正常范围内，无需过度焦虑，定期体检即可。
"""
    elif score >= 1:
        recommendations += """
- **中等代谢灵活性**：您携带部分保护性变异，代谢特征介于保护型和标准型之间。
- **饮食建议**：您对高热量饮食的耐受度略优于普通人，但仍建议控制精制碳水化合物的摄入。
- **运动建议**：规律的有氧运动配合力量训练，有助于最大化您的部分遗传保护效应。
"""
    else:
        recommendations += """
- **标准代谢特征**：您的GIPR基因型为人群中最常见的**标准型（野生型）**。这意味着您的代谢系统功能完整，对环境因素（如高热量饮食）非常敏感。
- **无额外遗传缓冲**：您没有额外的遗传变异来帮助抵抗肥胖风险。因此，**生活方式对您体重的决定作用比其他人更大**。
- **重点策略**：严格控制糖分和精制碳水摄入是关键，因为您的身体对GIP刺激的胰岛素反应是完整的，容易促进能量储存（脂肪合成）。
"""

    # 替泊泽肽相关建议
    recommendations += """
### 药物响应参考

如果您正在考虑或正在使用**替泊泽肽(Tirzepatide)**等肠促胰素类药物：

"""
    if gt_10423928.get('available') and gt_10423928.get('genotype') == 'AA':
        recommendations += """
- **增强响应 (Enhanced Sensitivity)**
  - 您的基因型（rs10423928-AA）在临床研究中与**更好的减重效果**相关。
  - **优势**：您可能对药物更敏感，在较低剂量下即可获得满意的疗效，或最终减重幅度超过平均水平。
  - **注意**：药物敏感性增加也可能意味着需要更密切关注剂量调整，请务必遵医嘱。
"""
    elif gt_10423928.get('available') and gt_10423928.get('genotype') in ['AT', 'TA']:
        recommendations += """
- **良好响应 (Good Response)**
  - 作为杂合子携带者，您对药物的响应预计优于标准型人群。
  - **预期**：您有望获得良好的体重减轻效果，疗效可能介于标准响应和增强响应之间。
  - **建议**：配合生活方式干预，可进一步放大药物疗效。
"""
    else:
        recommendations += """
- **标准响应 (Standard Response)**
  - **解读**：您的基因型是**标准型**，这意味着您对药物**不抵抗**，但也**没有额外的遗传加成**。
  - **预期**：您的预期疗效符合临床试验报道的平均水平（例如SURMOUNT系列研究的平均数据）。
  - **关键点**：由于缺乏遗传上的“助推力”，**严格的饮食控制和运动配合**对于您获得理想的减重效果至关重要。药物是有效的工具，但您的生活方式依从性决定了最终效果的上限。
"""

    return recommendations


def generate_simple_report(results):
    """
    生成简化版报告（用于数据缺失较多的情况）

    Args:
        results: dict, analyze_genotypes的返回结果

    Returns:
        str: Markdown格式的简化报告
    """
    report = """# GIPR 靶点基因解读报告

## 数据状态

很抱歉，您的基因数据不足以完成完整的GIPR靶点分析。

"""
    report += f"**检测覆盖率**: {results['available_count']}/{results['total_count']} 个位点\n\n"

    report += """### 位点检测状态

| 位点 | 状态 |
|------|------|
"""
    for gene_key, gt_info in results['genotypes'].items():
        status = "已检测" if gt_info['available'] else "未检测"
        report += f"| {gt_info['rsid']} | {status} |\n"

    report += """

## 建议

- 如果您的芯片版本不支持这些位点，可能需要升级检测
- 部分位点可能在您的基因数据中缺失
- 如有疑问，请联系WeGene客服

---

## 免责声明

本报告仅基于有限的基因位点信息提供参考性解读，不能作为医学诊断或治疗依据。

**本解读由WeGene轻应用自动生成，仅供参考。**
"""
    return report
