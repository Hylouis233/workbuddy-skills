---
name: ph-sitrep
display_name: 监测快报
display_name_en: Situation Note
description: "Draft a short public-health situation note from epic-harness output or a de-identified table. Use for sitrep, monitoring brief, or what changed in the public event list."
description_zh: "用 epic-harness 的当次公开监测结果或脱敏表写一页监测快报，写明数据状态、本期信号和缺口。"
description_en: "Write a one-page monitoring note that keeps event counts separate from case counts."
category: writing
version: 1.0.0
author: Hylouis233
allowed-tools: Bash,Read
---
# 监测快报

要把当前公开监测收成一页内部快报时用这个技能。标题用“监测快报”，不用“预警”。

## 数字从哪来

实时监测数字只从已安装的 `epic-harness` 刚跑完的输出里抄。查询命令以那个技能的 `SKILL.md` 为准。用户给出的脱敏表也可以当数字来源，报告里写上文件名。

两边对不上的数分开写：EpicDemic 的一行是事件，EpicIntel 的汇总才可能是病例或死亡。空着的数不要写成零。接口失败或表里没有的数留空，不改用记忆。

这是监测整理，不是诊断，也不是官方预警。不调用管理员、登录、审批、发布或告警外发接口。

## 步骤

1. 先写查询时间，以及 EpicIntel 健康检查是否成功。健康检查失败时，快报开头只写这个状态。
2. 本期信号用一张短表：日期、病种、地点、口径、数量、来源、站点。
3. 和上一期相比，只比较用户或上一份输出里已经有的同一口径数字。没有上一期就写“无可比上期”。
4. 缺口单独列：缺日期、缺地点、缺数量口径、来源机构为空。

## 输出

```markdown
# 监测快报
查询时间：
数据状态：
本期信号：
与上期相比：
缺口：
说明：公开来源监测整理，不是诊断，也不是官方预警。
```
