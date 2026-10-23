---
name: ph-risk-bulletin
display_name: 风险摘记
display_name_en: Risk Note
description: "Write an internal monitoring note about uncertainty and gaps in public epidemic signals. Use for a risk note or bulletin draft. It is not an official warning."
description_zh: "根据已核对的公开监测写内部风险摘记，列出已看到的信号、不确定的地方和需要人工核对的问题。"
description_en: "Draft an internal note that lists known signals and open questions without issuing an alert."
category: writing
version: 1.0.0
author: Hylouis233
allowed-tools: Bash,Read
---
# 风险摘记

需要把已核对的信号写成给同事看的摘记时用这个技能。标题用“风险摘记”。

## 数字从哪来

实时监测数字只从已安装的 `epic-harness` 刚跑完的输出里抄。查询命令以那个技能的 `SKILL.md` 为准。用户给出的脱敏表也可以当数字来源，报告里写上文件名。

两边对不上的数分开写：EpicDemic 的一行是事件，EpicIntel 的汇总才可能是病例或死亡。空着的数不要写成零。接口失败或表里没有的数留空，不改用记忆。

这是监测整理，不是诊断，也不是官方预警。不调用管理员、登录、审批、发布或告警外发接口。

## 步骤

1. 已看到的内容只复述分诊表或快报里的行。
2. 不确定的地方写成问题：数量口径是不是病例、地点是不是暴露地、来源能不能打开。
3. 需要人工核对的事项用问句，不写成已经发布的措施。
4. 不写“向社会发布”或“已发出预警”。

## 输出

```markdown
# 风险摘记
范围：
已看到：
还不确定：
建议核对：
说明：内部监测摘记，不是诊断，也不是官方预警。
```
