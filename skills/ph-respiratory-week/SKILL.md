---
name: ph-respiratory-week
display_name: 呼吸道周报
display_name_en: Respiratory Week
description: "Summarize a weekly respiratory surveillance table without adding pathogens together or treating positivity as incidence. Use for influenza, COVID-19, RSV, or ILI percent."
description_zh: "整理流感、新冠、呼吸道合胞病毒或流感样病例百分比的周表。阳性率不是发病率，不同病原的阳性数不相加。"
description_en: "Report each respiratory pathogen on its own row and keep positivity separate from incidence."
category: data-analysis
version: 1.0.0
author: Hylouis233
allowed-tools: Bash,Read
---
# 呼吸道周报

用户给出一周的呼吸道监测表，或要求对照 `epic-harness` 的公开结果写周摘要时用这个技能。

## 数字从哪来

实时监测数字只从已安装的 `epic-harness` 刚跑完的输出里抄。查询命令以那个技能的 `SKILL.md` 为准。用户给出的脱敏表也可以当数字来源，报告里写上文件名。

两边对不上的数分开写：EpicDemic 的一行是事件，EpicIntel 的汇总才可能是病例或死亡。空着的数不要写成零。接口失败或表里没有的数留空，不改用记忆。

这是监测整理，不是诊断，也不是官方预警。不调用管理员、登录、审批、发布或告警外发接口。

表里如果有检测份数和阳性数，阳性率只等于同一病原、同一周的阳性数除以检测份数。检测份数为空时不计算阳性率。

流感样病例百分比是就诊或哨点定义下的百分比，不写成人群发病率。流感、新冠、呼吸道合胞病毒的阳性数各自成行，不相加，也不把相加结果叫作呼吸道感染总数。

没有用户提供的周表，且 `epic-harness` 的结果里也没有检测份数时，只列出已有的事件或病种行，阳性率和百分比都留空。
