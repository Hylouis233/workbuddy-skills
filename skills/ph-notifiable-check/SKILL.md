---
name: ph-notifiable-check
display_name: 法定目录核对
display_name_en: Notifiable List Check
description: "Check a disease name against a user-supplied current notifiable-disease catalog. Use when asked whether a disease is class A, B, or C in China. Do not answer the class from memory."
description_zh: "只根据用户提供的现行法定传染病目录核对病种类别。没有目录就不判断甲类、乙类或丙类。"
description_en: "Match a disease to a catalog file the user supplies, and leave the class blank when that file is absent."
category: data-analysis
version: 1.0.0
author: Hylouis233
allowed-tools: Bash,Read
---
# 法定目录核对

用户问某种病是不是甲类、乙类或丙类时用这个技能。类别只来自用户给出的现行目录行。

## 数字从哪来

实时监测数字只从已安装的 `epic-harness` 刚跑完的输出里抄。查询命令以那个技能的 `SKILL.md` 为准。用户给出的脱敏表也可以当数字来源，报告里写上文件名。

两边对不上的数分开写：EpicDemic 的一行是事件，EpicIntel 的汇总才可能是病例或死亡。空着的数不要写成零。接口失败或表里没有的数留空，不改用记忆。

这是监测整理，不是诊断，也不是官方预警。不调用管理员、登录、审批、发布或告警外发接口。

国家卫生健康委公布的现行传染病目录会调整。这个技能不内置类别表。

目录文件是 UTF-8 CSV，表头至少有 `disease,class`。可以另有 `source,as_of`。`source` 写目录文件或页面名称，`as_of` 写该目录的公布或读取日期。

```bash
python scripts/check_catalog.py --disease 登革热
python scripts/check_catalog.py --disease 登革热 --catalog catalog.csv
```

没有 `--catalog` 时，结果是 `unverified`，类别留空。有目录但没有这一行时，结果是 `not_in_catalog`，不要改用别的病种代替。

回答里附上脚本输出的 `source` 和 `as_of`。两个都空时，写明类别来自用户表格，但表格没有写来源日期。
