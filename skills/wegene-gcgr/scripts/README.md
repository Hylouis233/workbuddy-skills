# GCGR 靶点基因解读应用

WeGene 轻应用 - 解读 GCGR 基因变异对三重激动剂药物响应和代谢健康的影响

## 功能概述

本应用分析 GCGR 基因的 Gly40Ser (RS1801483) 变异，评估：

- **受体功能活性**：GCGR 受体的功能状态
- **三重激动剂响应**：对 GIP/GLP-1/GCGR 三重激动剂（如 瑞他鲁肽）的预期响应
- **人群特异性背景**：针对东亚人群的变异罕见性提示

## 检测位点

| rsID | 变异 | HGVS 描述 | 功能影响 | 东亚 MAF |
|------|------|------------|----------|----------|
| RS1801483 | Gly40Ser | c.118G>A, p.G40S | 降低胰高血糖素结合亲和力约3-4倍 | ~0% |

## 科学文献

- Hager J et al. Nature Genetics 1995; 9:299-304: 首次报道 GCGR Gly40Ser 突变与 NIDDM 的关联
- Hager J et al. Diabetologia 1995; 38:983-985: GCGR Gly40Ser 突变的种族异质性研究
- Ducluzeau PH et al. Acta Diabetologica 2000: Gly40Ser in Sardinian population
- ClinVar: RS1801483 分类为 Benign/Likely benign

## 三重激动剂药物

| 药物名称 | 开发状态 | 研发公司 |
|----------|----------|----------|
| 瑞他鲁肽 | III期临床 | 礼来 |
| UBT251 | 临床开发中 | 联邦制药 |
| BGM-0504 | 临床开发中 | 博瑞医药 |

## 本地测试

```bash
# 测试野生型
python main.py < test_wildtype.json

# 测试变异型
python main.py < test_variant.json

# 测试杂合型
python main.py < test_heterozygous.json

# 测试数据缺失
python main.py < test_missing.json
```

## 输入格式

```json
{
  "inputs": {
    "format": "wegene_affy_2",
    "RS1801483": "GG",
    "sex": 1,
    "age": 35
  }
}
```

## 输出格式

Markdown 格式的基因解读报告，包含：

1. 基因概览
2. 综合评估
3. 详细位点解读
4. 人群特异性说明
5. 三重激动剂响应预测
6. 个性化建议
7. 科学背景
8. 免责声明

## 部署

将以下文件打包为 `weapp.zip`：

```
weapp.zip
├── main.py           # 主程序
├── gene_data.py      # 基因数据定义
├── interpretation.py # 解读逻辑
├── report_generator.py # 报告生成
└── requirements.txt  # 依赖声明
```

## 注意事项

- GCGR Gly40Ser 变异在东亚人群中极罕见（MAF ~0%）
- 三重激动剂药物目前大多处于临床开发阶段
- 本报告仅供参考，不构成医疗建议

## 版本

v1.0 - 2024
