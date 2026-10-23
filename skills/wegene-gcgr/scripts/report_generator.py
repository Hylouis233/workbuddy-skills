# -*- coding: utf-8 -*-
"""
GCGR 靶点基因报告生成器
生成 Markdown 格式的基因解读报告
"""

from gene_data import GENES, LOCUS_ORDER, DISCLAIMER


def generate_report(results, recommendations):
    """
    生成完整的 Markdown 格式基因解读报告

    参数:
        results: 分析结果
        recommendations: 个性化建议列表

    返回:
        str: Markdown 格式的报告
    """
    report_parts = []

    # 1. 报告标题
    report_parts.append(generate_header())

    # 2. 综合评估
    report_parts.append(generate_comprehensive_assessment(results))

    # 3. 详细位点解读
    report_parts.append(generate_detailed_interpretation(results))

    # 4. 药物响应预测
    report_parts.append(generate_drug_response_section(results))

    # 5. 个性化建议
    report_parts.append(generate_recommendations(recommendations))

    # 6. 免责声明
    report_parts.append(DISCLAIMER)

    return '\n\n'.join(report_parts)


def generate_header():
    """生成报告标题"""
    return """# 🧬 GCGR 靶点基因与减重药物响应解读报告

本报告基于您的 **GCGR（胰高血糖素受体）基因多态性**，科学评估您的受体功能活性，并深度解析您对**以胰高血糖素受体激动为主要靶点的减重药物（如玛仕度肽和瑞他鲁肽）**的预期响应。

---"""


def generate_comprehensive_assessment(results):
    """生成综合评估部分"""
    activity_level = results['activity_level']
    available_count = results['available_count']
    total_count = results['total_count']

    # 活性等级对应的符号和颜色标签
    activity_emoji = {
        'normal_activity': '✅ **正常受体活性**',
        'mild_reduced_activity': '🟡 **受体活性轻微降低**',
        'reduced_activity': '🔴 **受体活性降低**',
        'unknown': '⚪ **未知**'
    }

    emoji_title = activity_emoji.get(activity_level['key'], '⚪ **未知**')

    assessment = f"""## 📊 综合评估

### 受体活性评估结果

> {emoji_title}

**💡 综合解读：** 
{activity_level['description']}"""

    return assessment


def generate_detailed_interpretation(results):
    """生成详细位点解读"""
    sections = ["## 🔍 详细基因位点解析"]

    genotype_results = results.get('genotypes', {})

    for gene_key in LOCUS_ORDER:
        if gene_key not in genotype_results:
            continue

        result = genotype_results[gene_key]
        if result is None:
            gene_info = GENES.get(gene_key, {})
            rsid = gene_info.get('rsid', gene_key)
            name = gene_info.get('name', gene_key)
            sections.append(f"""### {name} ({rsid})

- **您的基因型**：`数据缺失`
- **变异分类**：⚪ 无法评估

> **🧬 机制说明**：
> {gene_info.get('functional_impact', '暂无描述')}
> 
> **🧑‍⚕️ 科学解读**：
> 您的该位点数据缺失，无法进行准确的分子层面的功能评估。""")
            continue

        gene_info = result.get('gene_info', {})
        name = gene_info.get('name', gene_key)
        rsid = gene_info.get('rsid', gene_key)
        original_gt = result.get('original_genotype', result.get('sorted_genotype', '未知'))
        category = result.get('category', 'unknown')

        # 分类标签
        category_map = {
            'wildtype': '✅ 野生型 (正常功能)',
            'heterozygous': '⚠️ 杂合变异 (功能轻微改变)',
            'variant': '⚠️ 纯合变异 (功能显著降低)',
            'unknown': '⚪ 未知'
        }
        category_label = category_map.get(category, '⚪ 未知')

        sorted_gt = result.get('sorted_genotype', '')
        interpretation = gene_info.get('interpretation', {}).get(sorted_gt, '暂无解读')

        section = f"""### {name} ({rsid})

- **您的基因型**：`{original_gt}`
- **变异分类**：{category_label}

> **🧬 机制说明**：
> {gene_info.get('functional_impact', '暂无描述')}
> 
> **🧑‍⚕️ 科学解读**：
> {interpretation}"""

        sections.append(section)

    return '\n\n'.join(sections)


def generate_drug_response_section(results):
    """生成胰高血糖素受体激动剂药物响应预测部分"""
    prediction = results.get('gcgr_agonist_prediction', {})
    activity_level = results.get('activity_level', {})

    section = f"""## 💊 药物响应预测

玛仕度肽（Mazdutide）和瑞他鲁肽（Retatrutide）是本位点最具代表性的新型减重药物，其核心机制之一是通过激动 **GCGR（胰高血糖素受体）** 来大幅提升人体的静息代谢率，增加能量消耗，从而实现强效减重。您本身的 GCGR 基因多态性直接决定了该药物在该靶点上的发挥效率。

### 靶向响应预测结果

- **🎯 整体响应预期**：**{prediction.get('overall_response', '无法预测')}**
- **⚙️ GCGR 通路贡献度**：{prediction.get('gcgr_contribution', '无法评估')}

**📝 药物建议**：
{activity_level.get('gcgr_agonist_response', '无法预测')}"""

    # 添加药物建议
    drug_recs = prediction.get('drug_recommendations', [])
    if drug_recs:
        section += "\n\n### 🔬 临床用药参考提示\n\n"
        for rec in drug_recs:
            section += f"- **基因契合度**：**{rec['suitability']}**\n- **科学建议**：{rec['note']}\n"

    section += """
> ⚠️ **注意**：本预测仅基于您的 GCGR 单一基因多态性特征进行推演。药物在人体内的实际代谢与疗效极其复杂，涉及众多基因与环境因素。本内容仅供医学科普与健康参考，**绝不能替代执业医师的处方与临床诊断**。请务必在专业医生的指导下制定您的减重用药方案。"""

    return section


def generate_recommendations(recommendations):
    """生成个性化建议部分"""
    if not recommendations:
        return ""

    section = """## 📌 科学减重与健康管理建议

基于您的 GCGR 基因功能特征，我们为您定制了以下健康管理策略：
"""
    for rec in recommendations:
        category = rec.get('category', '一般建议')
        content = rec.get('content', '')
        section += f"\n### 🔸 {category}\n{content}\n"

    return section
