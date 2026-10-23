# -*- coding: utf-8 -*-
"""
GIP 靶点基因解读 WeGene 轻应用
主程序入口
"""

import sys
import json

from gene_data import REQUIRED_RSIDS
from interpretation import analyze_genotypes
from report_generator import generate_report


def main():
    """主函数"""
    # 从 stdin 读取输入数据
    body = sys.stdin.read()

    try:
        inputs = json.loads(body)['inputs']
    except Exception as e:
        sys.stderr.write('输入数据格式错误，请检查JSON格式')
        sys.exit(2)

    try:
        # 分析基因型数据
        results = analyze_genotypes(inputs)

        # 检查是否有足够的有效位点
        if results['available_count'] == 0:
            sys.stderr.write('很抱歉，您的基因数据不完整，暂时无法进行GIPR靶点分析。需要以下位点的基因型数据: RS10423928, RS1800437, RS11672660')
            sys.exit(2)

        # 生成报告
        report = generate_report(results)

        # 输出报告（只能 print 一次）
        print(report)

    except Exception as e:
        sys.stderr.write('分析过程中遇到错误：{}'.format(str(e)))
        sys.exit(2)


if __name__ == '__main__':
    main()
