from gene_data import VARIANTS, RISK_CATEGORIES, LOCUS_ORDER

def normalize_genotype(genotype):
    if not genotype or genotype in ['--', '__', 'NC', '']:
        return 'unknown'
    genotype = genotype.upper().strip()
    if len(genotype) != 2:
        return None
    return ''.join(sorted(genotype))

def get_variant_status(rsid, genotype):
    if rsid not in VARIANTS:
        return 'unknown'
    variant = VARIANTS[rsid]
    ref = variant.get('reference_allele', '')
    var = variant.get('variant_allele', '')
    if not ref or not var:
        return 'unknown'
    gt = normalize_genotype(genotype)
    if not gt:
        return 'unknown'
    if var in gt:
        return 'pathogenic'
    if gt == ref + ref:
        return 'wildtype'
    return 'wildtype'

def analyze_men2_risk(inputs):
    results = {
        'pathogenic_variants': [],
        'wildtype_variants': [],
        'unknown_variants': [],
        'highest_risk': None,
        'highest_risk_category': None,
        'ata_category': None,
        'subtype': [],
        'available_count': 0,
        'total_count': len(LOCUS_ORDER),
        'variant_details': {}
    }
    for rsid in LOCUS_ORDER:
        if rsid not in VARIANTS:
            continue
        variant = VARIANTS[rsid]
        input_key = variant.get('input_key', rsid.upper())
        genotype = inputs.get(input_key) or inputs.get(rsid) or inputs.get(rsid.upper())
        status = get_variant_status(rsid, genotype)
        results['variant_details'][rsid] = {
            'rsid': rsid,
            'input_key': input_key,
            'genotype': genotype,
            'status': status,
            'codon': variant.get('codon'),
            'protein_change': variant.get('protein_change'),
            'aa_change': variant.get('aa_change'),
            'ata_risk': variant.get('ata_risk'),
            'risk_level': variant.get('risk_level'),
            'clinical_significance': variant.get('clinical_significance'),
            'clinical_notes': variant.get('clinical_notes'),
            'subtype': variant.get('subtype', []),
            'verification_status': variant.get('verification_status')
        }
        if status == 'pathogenic':
            results['pathogenic_variants'].append(rsid)
            results['available_count'] += 1
            ata_risk = variant.get('ata_risk', 'ATA-MOD')
            current_priority = get_risk_priority(ata_risk)
            highest_priority = get_risk_priority(results['ata_category'] or 'ATA-MOD')
            if current_priority > highest_priority:
                results['ata_category'] = ata_risk
                results['highest_risk'] = variant.get('risk_level')
                results['highest_risk_category'] = RISK_CATEGORIES.get(ata_risk, {})
            for st in variant.get('subtype', []):
                if st not in results['subtype']:
                    results['subtype'].append(st)
        elif status == 'wildtype':
            results['wildtype_variants'].append(rsid)
            results['available_count'] += 1
        else:
            results['unknown_variants'].append(rsid)
    if not results['pathogenic_variants']:
        results['highest_risk'] = '未检出致病突变'
        results['ata_category'] = None
        results['subtype'] = []
    return results

def get_risk_priority(ata_category):
    priorities = {
        'ATA-HST': 3,
        'ATA-H': 2,
        'ATA-MOD': 1
    }
    return priorities.get(ata_category, 0)

def get_clinical_recommendation(results):
    if not results['pathogenic_variants']:
        return {
            'urgency': 'routine',
            'recommendation': '本次筛查未发现 MEN2 相关的高风险基因突变。建议您保持健康的生活方式和常规体检。',
            'actions': [
                '定期进行常规体检，关注甲状腺健康',
                '若有明确的家族病史，建议咨询专业医生进行更全面的评估'
            ]
        }
    ata = results['ata_category']
    if ata == 'ATA-HST':
        return {
            'urgency': 'urgent',
            'recommendation': '检测到可能与 MEN2 高度相关的基因变异，属于 ATA 指南中的最高风险等级。',
            'actions': [
                '建议您尽快前往内分泌科或头颈外科就诊咨询',
                '请医生评估是否需要进行进一步的生化检查（如降钙素）或影像学检查',
                '建议您的直系亲属也咨询专业医生，评估是否需要进行相关筛查'
            ]
        }
    elif ata == 'ATA-H':
        return {
            'urgency': 'high',
            'recommendation': '检测到可能与 MEN2 相关的基因变异，属于 ATA 指南中的高风险等级。',
            'actions': [
                '建议您尽早咨询内分泌专科医生',
                '医生可能会建议进行定期的甲状腺监测',
                '建议告知家族成员，必要时进行咨询'
            ]
        }
    elif ata == 'ATA-MOD':
        return {
            'urgency': 'moderate',
            'recommendation': '检测到可能与 MEN2 相关的基因变异，属于 ATA 指南中的中等风险等级。',
            'actions': [
                '建议您在常规体检中关注甲状腺指标',
                '咨询专业医生，制定适合您的长期健康监测计划',
                '保持关注，定期复查'
            ]
        }
    else:
        return {
            'urgency': 'routine',
            'recommendation': '建议咨询遗传咨询师或内分泌专科医生获取个性化建议。',
            'actions': [
                '咨询专业医生',
                '完善相关检查'
            ]
        }
