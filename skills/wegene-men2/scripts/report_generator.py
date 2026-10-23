from gene_data import RISK_CATEGORIES, UNSUPPORTED_VARIANTS
from interpretation import get_clinical_recommendation

def generate_men2_report(results):
    sections = [
        generate_header(),
        generate_summary_section(results),
        generate_risk_assessment(results),
        generate_variant_details(results),
        generate_recommendations(results),
        generate_disclaimer()
    ]
    return '\n\n'.join(sections)

def generate_header():
    return """# MEN2/MTC 基因筛查报告"""


def generate_summary_section(results):
    pathogenic_count = len(results['pathogenic_variants'])
    wildtype_count = len(results['wildtype_variants'])
    total_count = results['total_count']
    if pathogenic_count == 0:
        summary = """## 1. 检测摘要

### 检测结果: 未检出 RET 基因高风险突变

在本次涵盖的 9 个 MEN2 核心风险位点中，您的基因型均为**野生型**（未携带已知致病变异）。

**这意味着什么？**
- 您罹患 MEN2 相关遗传性甲状腺髓样癌 (MTC) 的风险显著低于携带者。
- 但由于基因检测技术的局限性，这并不能完全排除所有患病风险（详见下方“局限性”说明）。"""
    else:
        subtypes = '、'.join(results['subtype']) if results['subtype'] else 'MEN2'
        summary = """## 1. 检测摘要

### 检测结果: ⚠️ 检出 RET 基因风险突变

**检出突变数**: {} 个
**相关亚型**: {}
**风险等级**: {}

**这意味着什么？**
- 检测结果提示您携带了与 MEN2 相关的 RET 基因变异。
- 这可能会增加您罹患甲状腺髓样癌 (MTC) 及相关内分泌疾病的风险。
- 请务必仔细阅读下方的“风险评估”与“临床建议”，并尽快咨询专业医生。""".format(
            pathogenic_count,
            subtypes,
            results['highest_risk'] or '待评估'
        )
    
    summary += """

**位点覆盖率**: {}/{} (核心致病位点)""".format(
        results['available_count'], total_count
    )
    return summary

def generate_risk_assessment(results):
    if not results['pathogenic_variants']:
        return """## 2. 风险评估

**您的评估结果**: **低风险 (未检出)**

根据 ATA 2015 指南，本次检测未发现您携带 M918T、C634 等高风险致病突变。

**结果解读**:
- **排除高危**: 基本排除了最常见且最危险的 MEN2B 和 MEN2A 高风险亚型。
- **仍需注意**: 阴性结果不能完全替代临床诊断。如果您有甲状腺髓样癌家族史，即使检测结果为阴性，仍建议咨询遗传咨询师进行更全面的测序分析。"""
    
    ata = results['ata_category']
    risk_category = results['highest_risk_category'] or {}
    
    risk_level_display = {
        'ATA-HST': '**最高风险等级 (HST)**',
        'ATA-H': '**高风险等级 (H)**',
        'ATA-MOD': '**中等风险等级 (MOD)**'
    }.get(ata, '**待进一步评估**')
    
    assessment = """## 2. 风险评估

**ATA 风险分级**: {}

**分级说明**:
{}

**什么是 ATA 分级？**
美国甲状腺协会 (ATA) 根据 RET 基因突变与甲状腺髓样癌 (MTC) 的相关性强弱，将突变分为三个等级：
- **最高风险 (HST)**: 极高侵袭性，建议婴幼儿期干预。
- **高风险 (H)**: 高侵袭性，建议学龄前干预。
- **中等风险 (MOD)**: 风险相对较低，可根据监测情况决定。""".format(
        risk_level_display,
        risk_category.get('description', '请咨询专业医生进行解读')
    )
    return assessment

def generate_variant_details(results):
    details = results['variant_details']
    if results['pathogenic_variants']:
        section = """## 3. 检出的致病突变详情

| 位点 | 氨基酸改变 | 风险等级 | 临床意义 |
|------|----------|----------|----------|"""
        for rsid in results['pathogenic_variants']:
            v = details[rsid]
            section += """
| {} | {} | {} | {} |""".format(
                rsid.upper(),
                v.get('protein_change', '-'),
                v.get('risk_level', '-'),
                v.get('clinical_significance', '-')
            )
        section += "\n\n**临床注释**:"
        for rsid in results['pathogenic_variants']:
            v = details[rsid]
            notes = v.get('clinical_notes', '')
            if notes:
                section += "\n- **{}**: {}".format(v.get('protein_change', rsid), notes)
    else:
        section = """## 3. 检测位点详情

本次检测覆盖的 9 个 RET 基因核心位点均为**野生型** (未发生致病突变)。"""
    return section

def generate_recommendations(results):
    recommendation = get_clinical_recommendation(results)
    urgency_display = {
        'urgent': '🔴 **建议立即关注**',
        'high': '🟠 **建议密切关注**',
        'moderate': '🟡 **建议常规关注**',
        'routine': '🟢 **常规生活建议**'
    }.get(recommendation['urgency'], '-')
    
    section = """## 4. 个性化健康建议

**关注等级**: {}

**核心建议**:
> {}

**详细建议措施**:""".format(
        urgency_display,
        recommendation['recommendation']
    )
    for action in recommendation['actions']:
        section += "\n- {}".format(action)
    return section

def generate_disclaimer():
    return """## 6. 重要声明与局限性

    1. 筛查性质声明: 
    本报告属于消费级基因检测结果，仅供健康管理参考，绝不能替代临床医疗诊断。任何医疗决策（如手术、用药）请务必咨询内分泌科或头颈外科医生。

    2. 检测局限性: 
    本检测仅覆盖了 ATA 指南中明确的 9 个核心高风险位点。虽然这覆盖了绝大多数 MEN2B 和 MEN2A 病例，但阴性结果并不能完全排除患病可能。罕见突变、大片段缺失或新的未知突变可能无法被检出。

    3. 适用人群: 
    本应用适用于关注甲状腺健康的普通人群进行风险筛查。如果您已有明确的甲状腺髓样癌家族史，建议直接前往医院进行全基因测序。"""
