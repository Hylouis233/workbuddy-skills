---
name: ph-vector-signal
display_name: 病媒信号
display_name_en: Vector Signal
description: "Separate human disease events from vector-density figures in a monitoring note. Use for dengue, malaria, Japanese encephalitis, or mosquito signals. Do not forecast cases from a vector index."
description_zh: "把人群疾病事件和用户另行提供的蚊媒密度分开写。适用于登革热等病媒信号，不用密度指数推算病例。"
description_en: "Keep human event rows separate from a supplied vector index, without forecasting cases."
category: data-analysis
version: 1.0.0
author: Hylouis233
allowed-tools: Bash,Read
---
# 病媒信号

信号涉及登革热、疟疾、流行性乙型脑炎或其他明确由病媒相关的疾病时用这个技能。

## 数字从哪来

实时监测数字只从已安装的 `epic-harness` 刚跑完的输出里抄。查询命令以那个技能的 `SKILL.md` 为准。用户给出的脱敏表也可以当数字来源，报告里写上文件名。

两边对不上的数分开写：EpicDemic 的一行是事件，EpicIntel 的汇总才可能是病例或死亡。空着的数不要写成零。接口失败或表里没有的数留空，不改用记忆。

这是监测整理，不是诊断，也不是官方预警。不调用管理员、登录、审批、发布或告警外发接口。

1. 人群事件仍按 `epic-harness` 或脱敏表的一行一条列出。
2. 布雷图指数、成蚊密度或其他密度数，只有用户在表里给出才写入，并注明表的名称和日期。没有密度数就写“未提供”。
3. 不把密度指数换成预期病例数，也不把不同病种的事件相加。
4. 不写杀虫剂配比、孳生地用药或病原分离步骤。防制措施写“由属地部门按现行方案安排”。

输出两张表：`人群事件` 和 `病媒密度`。第二张没有数时保留表头并写未提供。
