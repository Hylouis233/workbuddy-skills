import sys
import json
from gene_data import VARIANTS, RISK_CATEGORIES
from interpretation import analyze_men2_risk
from report_generator import generate_men2_report

def main():
    body = sys.stdin.read()
    try:
        data = json.loads(body)
        inputs = data.get('inputs', {})
        results = analyze_men2_risk(inputs)
        if results['available_count'] == 0:
            sys.stderr.write('很抱歉，您的基因数据中缺少 RET 基因的相关位点信息,暂时无法生成解读报告。请确保您的基因检测数据包含 RET 基因位点。')
            sys.exit(2)
        report = generate_men2_report(results)
        print(report)
    except json.JSONDecodeError as e:
        sys.stderr.write('输入数据格式错误:无法解析 JSON 数据。请检查输入格式是否正确。')
        sys.exit(2)
    except KeyError as e:
        sys.stderr.write('输入数据结构错误:缺少必要的数据字段。')
        sys.exit(2)
    except Exception as e:
        error_message = '分析过程中遇到错误:{}'.format(str(e))
        sys.stderr.write(error_message)
        sys.exit(2)

if __name__ == '__main__':
    main()
