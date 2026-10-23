---
name: ph-linelist-qa
display_name: 一览表质检
display_name_en: Linelist Check
description: "Check a CSV linelist and stop when a name, phone, identity-document, or street-address column or value is present. Use before counting cases from a line list."
description_zh: "检查病例一览表是否含姓名、电话、证件号或门牌。发现这类列或值就停止，只报告列名、行号和计数。"
description_en: "Stop a line-list analysis when direct identifiers are present, and otherwise report counts only."
category: data-analysis
version: 1.0.0
author: Hylouis233
allowed-tools: Bash,Read
---
# 一览表质检

用户要按一份病例一览表计数之前，先跑这个技能。

## 数字从哪来

实时监测数字只从已安装的 `epic-harness` 刚跑完的输出里抄。查询命令以那个技能的 `SKILL.md` 为准。用户给出的脱敏表也可以当数字来源，报告里写上文件名。

两边对不上的数分开写：EpicDemic 的一行是事件，EpicIntel 的汇总才可能是病例或死亡。空着的数不要写成零。接口失败或表里没有的数留空，不改用记忆。

这是监测整理，不是诊断，也不是官方预警。不调用管理员、登录、审批、发布或告警外发接口。

```bash
python scripts/linelist_qa.py linelist.csv
python scripts/linelist_qa.py linelist.csv --date-column onset_date --id-column case_id
```

脚本只打印列名、行号和计数。出现姓名、电话、证件号、详细住址或门牌这类列，或单元格本身像证件号、手机号时，状态是 `stopped`，不再继续计数或写报告。

通过以后，才可以把同一文件交给 `ph-epicurve`。病例定义、纳入和排除由用户给出；文件没写的分层不要补。
