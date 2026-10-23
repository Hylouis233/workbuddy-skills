---
name: ph-signal-triage
display_name: 信号分诊
display_name_en: Signal Triage
description: "Triage public epidemic signals from an epic-harness result or a de-identified table. Use for signal triage, sorting outbreak events, and separating events from case counts."
description_zh: "把 epic-harness 的公开监测结果或一份脱敏表整理成分诊表，分开事件和病例，标出缺数量和来源弱的信号。"
description_en: "Sort public monitoring signals into a short triage table without inventing counts or issuing an alert."
category: data-analysis
version: 1.0.0
author: Hylouis233
allowed-tools: Bash,Read
---
# 信号分诊

用户拿来一批疫情信号，要先看哪些值得接着核、哪些还不能计数时用这个技能。

## 数字从哪来

实时监测数字只从已安装的 `epic-harness` 刚跑完的输出里抄。查询命令以那个技能的 `SKILL.md` 为准。用户给出的脱敏表也可以当数字来源，报告里写上文件名。

两边对不上的数分开写：EpicDemic 的一行是事件，EpicIntel 的汇总才可能是病例或死亡。空着的数不要写成零。接口失败或表里没有的数留空，不改用记忆。

这是监测整理，不是诊断，也不是官方预警。不调用管理员、登录、审批、发布或告警外发接口。

## 步骤

1. 用 `epic-harness` 取当前列表。用户已经给了表就用那张表，不再另查一套数字。
2. 每一行只标一个状态：`新出现`、`仍在列表`、`缺数量`、`来源未写明`。状态只根据这一行有没有日期、地点、病种、数量口径和来源机构。
3. `scale` 或正文里的数字，先看它写的是事件、病例还是死亡。看不出来就放进 `缺数量`，不要换算。
4. 不打风险分，不排序成“高中低预警”。

## 输出

`日期 | 病种 | 地点 | 口径 | 状态 | 来源机构 | 站点或文件`

表后写过滤条件、用了多少行、还有多少行因为缺字段没有进入表。
