---
name: ph-epicurve
display_name: 周流行曲线
display_name_en: Weekly Epicurve
description: "Build a weekly count table from a de-identified date column. Use for an epidemic curve, weekly bins, or onset dates. Rows are events or cases only when the file says so."
description_zh: "把脱敏表里的日期按周一为一周的起点计数。适用于流行曲线和周分布，不把空日期当成零，也不把事件行当成病例。"
description_en: "Count a date column by ISO week and report missing dates separately."
category: data-analysis
version: 1.0.0
author: Hylouis233
allowed-tools: Bash,Read
---
# 周流行曲线

用户有一份带日期的脱敏表，要看按周计数时用这个技能。

## 数字从哪来

实时监测数字只从已安装的 `epic-harness` 刚跑完的输出里抄。查询命令以那个技能的 `SKILL.md` 为准。用户给出的脱敏表也可以当数字来源，报告里写上文件名。

两边对不上的数分开写：EpicDemic 的一行是事件，EpicIntel 的汇总才可能是病例或死亡。空着的数不要写成零。接口失败或表里没有的数留空，不改用记忆。

这是监测整理，不是诊断，也不是官方预警。不调用管理员、登录、审批、发布或告警外发接口。

一行是什么，以文件或 `epic-harness` 的口径为准。EpicDemic 导出的一行是事件。不要把 `scale` 加进周计数，除非用户写明该列是同一口径的病例数。

```bash
python scripts/weekly_bins.py events.csv
python scripts/weekly_bins.py events.csv --date-column onset_date
```

日期列会依次尝试 `original_date`、`onset_date`、`date`、`发病日期`、`日期`。周从星期一开始。缺日期和无法解析的日期分开计数，不计入任何一周，也不写成零。

曲线形状只用来提出下一个问题，例如是否要核对现行监测方案里的时间窗口。不根据形状判断传播方式，不填写潜伏期或代际间隔。
