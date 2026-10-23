---
name: ph-cluster-notes
display_name: 聚集性记录
display_name_en: Cluster Notes
description: "Record the fields of a foodborne or other cluster from de-identified information the user already has. Use for a cluster note or outbreak field list. No laboratory methods."
description_zh: "按用户已有的脱敏信息记录聚集性或食源事件的时间、地点、暴露人数和发病人数。不写采样、培养或检测步骤。"
description_en: "Fill a cluster field list from supplied de-identified facts, without laboratory procedures."
category: writing
version: 1.0.0
author: Hylouis233
allowed-tools: Bash,Read
---
# 聚集性记录

用户要整理一起聚餐、学校、单位或其他共同暴露事件的字段时用这个技能。先对一览表使用 `ph-linelist-qa`。质检没有通过就不记录。

## 数字从哪来

实时监测数字只从已安装的 `epic-harness` 刚跑完的输出里抄。查询命令以那个技能的 `SKILL.md` 为准。用户给出的脱敏表也可以当数字来源，报告里写上文件名。

两边对不上的数分开写：EpicDemic 的一行是事件，EpicIntel 的汇总才可能是病例或死亡。空着的数不要写成零。接口失败或表里没有的数留空，不改用记忆。

这是监测整理，不是诊断，也不是官方预警。不调用管理员、登录、审批、发布或告警外发接口。

只填用户已经给出的内容：

- 共同暴露的日期和场所类型，地点写到区县或场所类型
- 暴露人数、发病人数、首例和末例的发病时间
- 用户原文里的主要症状
- 可疑食品或水的名称
- 是否已送有资质机构：是、否或未知

人数缺一时留空。不补潜伏期，不写隔离或用药天数，不写采样、培养、核酸、毒素制备或配方。控制措施只写“由属地部门按现行方案决定”。
