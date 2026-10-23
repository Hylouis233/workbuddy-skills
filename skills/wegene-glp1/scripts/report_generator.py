# -*- coding: utf-8 -*-
"""
GLP-1 靶点基因报告生成器
生成 Markdown 格式的基因解读报告
"""

from gene_data import GENES, LOCUS_ORDER


def generate_report(risk_result, drug_response, recommendations, genotypes):
    """
    生成完整的 Markdown 格式基因解读报告

    参数:
        risk_result: 综合风险评估结果
        drug_response: 药物响应评估结果
        recommendations: 个性化建议列表
        genotypes: 用户基因型数据

    返回:
        str: Markdown 格式的报告
    """
    report_parts = []

    # 1. 报告标题
    report_parts.append(generate_header())

    # 2. 综合评估
    report_parts.append(generate_comprehensive_assessment(risk_result, drug_response))

    # 4. 详细位点解读
    report_parts.append(generate_detailed_interpretation(risk_result['locus_scores']))

    # 5. 药物响应评估
    report_parts.append(generate_drug_response_section(drug_response))

    # 6. 个性化建议
    report_parts.append(generate_recommendations(recommendations))

    # 7. 免责声明
    report_parts.append(generate_disclaimer())

    return '\n\n'.join(report_parts)


def generate_header():
    """生成报告标题"""
    return """# GLP-1 靶点基因解读报告

本报告基于您的 GLP1R 基因多态性，评估您对 GLP-1 通路的遗传特征，包括代谢风险和对 GLP-1 受体激动剂类药物的预期响应。

---"""


def generate_comprehensive_assessment(risk_result, drug_response):
    """生成综合评估部分"""
    risk_level = risk_result['risk_level']
    risk_pct = risk_result['risk_percentage']
    valid_loci = risk_result['valid_loci']
    total_loci = risk_result['total_loci']

    # 风险等级对应的符号 (使用ASCII兼容符号)
    risk_emoji = {
        'low': '[OK]',
        'moderate_low': '[--]',
        'moderate_high': '[+-]',
        'high': '[++]'
    }

    emoji = risk_emoji.get(risk_level['key'], '[?]')

    # 药物响应等级
    response_emoji = {
        'good': '[Good]',
        'moderate': '[Medium]',
        'poor': '[Poor]'
    }

    drug_emoji = response_emoji.get(drug_response['level'], '[?]')

    assessment = f"""## 综合评估

### 风险评估结果

{emoji} **综合风险等级：{risk_level['name']}**

| 指标 | 结果 |
|------|------|
| 风险评分 | {risk_pct}% |
| 有效位点数 | {valid_loci}/{total_loci} |

**解读：** {risk_level['description']}

### 药物响应预测

{drug_emoji} **GLP-1 受体激动剂响应：{drug_response['info']['name']}**

**解读：** {drug_response['info']['description']}"""

    return assessment


def generate_detailed_interpretation(locus_scores):
    """生成详细位点解读"""
    sections = ["## 详细位点解读", ""]

    for gene_key in LOCUS_ORDER:
        if gene_key not in locus_scores:
            continue

        locus = locus_scores[gene_key]
        gene_info = locus.get('gene_info', {})

        # 位点标题
        name = gene_info.get('name', gene_key)
        rsid = locus['rsid']
        genotype = locus.get('sorted_genotype', locus.get('genotype', '未知'))

        # 基因型类型 (使用ASCII兼容符号)
        type_map = {
            'protective': '[+] 保护型',
            'heterozygous': '[~] 杂合型',
            'risk': '[-] 风险型',
            'unknown': '[?] 未知'
        }
        type_label = type_map.get(locus['type'], '[?] 未知')

        section = f"""### {name}

| 属性 | 信息 |
|------|------|
| **位点编号** | {rsid} |
| **您的基因型** | {genotype} |
| **分类** | {type_label} |

**功能说明：** {gene_info.get('description', '暂无描述')}

**个人解读：** {locus.get('interpretation', '暂无解读')}"""

        sections.append(section)

    return '\n\n'.join(sections)


def generate_drug_response_section(drug_response):
    """生成药物响应评估部分"""
    details = drug_response.get('details', {})

    section = """## GLP-1 受体激动剂药物响应评估

### 药物基因组学相关位点

| 位点 | 您的基因型 | 预期响应 |
|------|-----------|----------|"""

    response_map = {
        'protective': '较好',
        'heterozygous': '中等',
        'risk': '较弱',
        'unknown': '您的数据缺失，无法评估'
    }

    for gene_key, detail in details.items():
        rsid = detail.get('rsid', gene_key)
        genotype = detail.get('genotype', '--')
        gt_type = detail.get('type', 'unknown')
        response = response_map.get(gt_type, '无法评估')

        section += f"\n| {rsid} | {genotype} | {response} |"

    section += f"""

### 用药建议

{drug_response['info']['description']}

> [!] **重要提示**：本评估仅供参考，实际用药方案应由专业医生根据您的具体情况制定。"""

    return section


def generate_recommendations(recommendations):
    """生成个性化建议部分"""
    section = """## 个性化建议

根据您的基因特征，我们提供以下个性化建议：

| 类别 | 建议 |
|------|------|"""

    for rec in recommendations:
        category = rec.get('category', '一般建议')
        content = rec.get('content', '')
        section += f"\n| **{category}** | {content} |"

    return section


def generate_disclaimer():
    """生成免责声明"""
    return """## 免责声明

本报告基于现有的科学研究和基因组学数据生成，仅供参考和教育目的，不构成医疗诊断或治疗建议。

**重要提示：**

1. 本报告中的风险评估基于有限的基因位点，不能完全代表您的整体健康状况
2. 基因只是影响健康的因素之一，生活方式、环境因素同样重要
3. 药物响应预测仅为参考，实际用药效果因人而异
4. 任何医疗决策应咨询专业医生，请勿自行调整用药方案
5. 本报告不适用于诊断、治疗、治愈或预防任何疾病"""
