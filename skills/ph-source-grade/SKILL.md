---
name: ph-source-grade
display_name: 来源分级
display_name_en: Source Grade
description: "Label the source strength of each public monitoring row from fields already present. Use when deciding how much a signal can support. Grades do not create new numbers."
description_zh: "按每一行已经写明的来源机构给公开监测信号分级。没有机构就标成来源未写明，不凭记忆升级。"
description_en: "Grade each row only from its recorded source fields."
category: data-analysis
version: 1.0.0
author: Hylouis233
allowed-tools: Bash,Read
---
# 来源分级

用户要判断一条公开信号能支撑到哪一步时用这个技能。

## 数字从哪来

实时监测数字只从已安装的 `epic-harness` 刚跑完的输出里抄。查询命令以那个技能的 `SKILL.md` 为准。用户给出的脱敏表也可以当数字来源，报告里写上文件名。

两边对不上的数分开写：EpicDemic 的一行是事件，EpicIntel 的汇总才可能是病例或死亡。空着的数不要写成零。接口失败或表里没有的数留空，不改用记忆。

这是监测整理，不是诊断，也不是官方预警。不调用管理员、登录、审批、发布或告警外发接口。

只看这一行已经有的 `source_org`、`source` 和正文：

| 级别 | 条件 |
| --- | --- |
| 机构已具名 | `source_org` 有机构名，或正文写了通报机构、日期和标题 |
| 仅有链接或媒体名 | 有 `source`，但没有机构名 |
| 来源未写明 | 两个字段都空，正文也没有可核对的出处 |

不因为病种常见就把级别升高。级别不改变数量。输出在原表后加一列“来源级别”。
