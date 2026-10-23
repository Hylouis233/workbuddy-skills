<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-03-07 | Updated: 2026-03-21 -->

# gip-app

## Purpose
GIPR 靶点基因解读 WeGene 轻应用。基于用户的 GIPR 基因多态性，评估 GIP 通路相关特征和对替泊泽肽(Tirzepatide)等肠促胰素类药物的预期响应。

## Key Files
| File | Description |
|------|-------------|
| `main.py` | 主程序入口，处理 stdin JSON 输入，调用分析模块，输出 Markdown 报告 |
| `gene_data.py` | GIPR 基因位点定义、评分等级、科学背景、免责声明 |
| `interpretation.py` | 评分算法、基因型分析、表型分离解读、替泊泽肽响应预测 |
| `report_generator.py` | Markdown 格式报告生成器，包含各报告章节生成函数 |
| `requirements.txt` | 依赖声明（无外部依赖，仅使用标准库） |
| `test_app.py` | 本地测试脚本，使用模拟数据验证完整流程 |
| `demo.json` | 测试数据文件，包含示例基因型输入 |
| `README.md` | 应用说明文档 |
| `wegene_utils.py` | WeGene 平台工具函数（平台提供） |

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| `__pycache__/` | Python 字节码缓存（自动生成） |

## For AI Agents

### Working In This Directory
- **架构**: `stdin (JSON) -> main.py -> stdout (Markdown)`
- **主入口**: `main.py` - 从 stdin 读取 JSON，输出报告到 stdout
- **输出规则**: 只能调用一次 `print()` 输出完整报告
- **错误处理**: 通过 `sys.stderr.write()` 输出错误信息
- **基因位点命名**: 使用大写 RS 号 (如 `RS10423928`)
- **基因型处理**: 杂合子需排序处理 (`AT` 和 `TA` 统一为 `AT`)

### Testing Requirements
```bash
# 本地测试
cat demo.json | python main.py

# 运行测试脚本
python test_app.py

# 预期输出: Markdown 格式的 GIPR 靶点基因解读报告
# 错误输出: stderr 非空时表示失败
```

### Common Patterns

**输入数据结构** (demo.json):
```json
{
  "inputs": {
    "sex": 1,
    "age": 30,
    "format": "wegene_affy_2",
    "RS10423928": "AT",
    "RS1800437": "GC",
    "RS11672660": "CT"
  }
}
```

**检测位点列表**:
| 位点 | 名称 | 权重 | 说明 |
|------|------|------|------|
| RS10423928 | GIP受体核心位点 | 1.5 | 影响剪接异构体和mRNA表达，存在表型分离现象 |
| RS1800437 | E354Q错义突变 | 1.2 | 与 rs10423928 完全连锁 |
| RS11672660 | 代谢综合征相关位点 | 1.0 | 与代谢综合征风险相关 |

**评分等级**:
| 等级 | 评分范围 | 分类 |
|------|----------|------|
| 高度保护型 | 4.0 - 6.0 | GIPR 功能偏向保护方向 |
| 中度保护型 | 2.0 - 3.9 | 一定保护效应 |
| 中性型 | 0.5 - 1.9 | 基线水平 |
| 风险型 | 0.0 - 0.4 | 存在代谢风险 |

**基因型有效性检查**:
```python
def is_valid_genotype(genotype):
    if not genotype:
        return False
    genotype = genotype.upper()
    return genotype not in ['--', '__', '']
```

**基因型排序处理**:
```python
def sort_genotype(genotype):
    if genotype and len(genotype) == 2:
        return ''.join(sorted(genotype.upper()))
    return genotype
```

### Output Format
生成完整的 Markdown 格式报告，包含以下章节:
1. 标题: `# GIPR 靶点基因解读报告`
2. 基因概览: GIPR 功能介绍和位点检测状态
3. 综合评估: 评分结果和替泊泽肽响应预测
4. 详细位点解读: 每个位点的基因型、分类、解读
5. 表型分离现象说明: rs10423928 的特殊效应
6. 个性化建议: 代谢健康管理和药物响应参考
7. 科学背景: GIPR 基因与肠促胰素系统
8. 免责声明

## Dependencies

### Internal
- 父目录: `G:\wegene\apps\` - WeGene 轻应用集合
- 模块依赖: `gene_data` -> `interpretation` -> `report_generator`

### External
- 无外部依赖，仅使用 Python 标准库
- 平台约束: 执行时间 120s, 代码包 10MB, 输出 1MB

## Special Notes

### 表型分离现象
rs10423928 位点展示了一种经典的"表型分离"效应:
- A 等位基因与更低的 BMI 相关（保护效应）
- A 等位基因与 GIP 刺激的胰岛素分泌受损相关（风险效应）
- 两种效应相互抵消，整体 2 型糖尿病风险中性

### 连锁不平衡
rs1800437 与 rs10423928 存在完全连锁不平衡，两者提供的信息高度相关。

### 替泊泽肽 (Tirzepatide)
替泊泽肽是首个获批的双重 GIPR/GLP-1R 激动剂，对两个通路同时起作用。GIPR 基因型可能影响药物响应。

<!-- MANUAL: -->
