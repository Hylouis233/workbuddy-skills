# WorkBuddy skills

Hylouis233 公开的 WorkBuddy 技能包。每个技能目录都有 `SKILL.md`。`packages/` 里是对应的 zip，压缩包内是 `<skill-name>/SKILL.md`。

## 本次公开

| 技能 | 来源 | 说明 |
| --- | --- | --- |
| `skills/weapp-researcher` | 私有仓库 wegene 中的研究员技能 | 只公开工作流，不包含凭证 |
| `skills/wegene-gcgr` `wegene-gip` `wegene-glp1` `wegene-men2` | wegene 的四个轻应用 | 脚本只接受合成基因型 |
| `skills/hello-mcode` | MiniMax-Code-Plugins 示例 | Apache-2.0 |
| `skills/minimax-code-trajectory` | hetaoBackend 的插件 | 作者仍是 hetaoBackend，Apache-2.0 |
| `skills/epic-harness` | 新建 | 只读连接 EpicDemic 与 EpicIntel 的公开 HTTP 接口 |

`catalog/` 是 mcodeforlegal、openscience、open-protein-binder-design、bibverify、dsh-magpie、magpie-quota，以及 MiniMax-Code-Plugins 里 Hylouis233 三个插件的 WorkBuddy 元数据补齐版。

## 站点连接

`epic-harness` 连接：

- https://epicdemic.hylouis.top/
- https://epicintel.hylouis.top/

这两个网站没有单独的 MCP URL。技能调用它们的公开只读接口，并避开内部 MCP 的审批、发布和告警外发工具。

## 公共卫生监测

下面 10 个技能做监测整理。实时数字从 `epic-harness` 的当次输出抄，或从用户给出的脱敏表抄。事件和病例分开写。它们不判断诊断，也不发布预警。

| 技能 | 用途 |
| --- | --- |
| `ph-signal-triage` | 把公开信号分成新出现、仍在列表、缺数量、来源未写明 |
| `ph-sitrep` | 写一页监测快报 |
| `ph-notifiable-check` | 只按用户提供的现行目录核对甲乙丙类 |
| `ph-epicurve` | 按周计数，缺日期单独列出 |
| `ph-risk-bulletin` | 写内部风险摘记 |
| `ph-linelist-qa` | 一览表出现姓名、电话、证件号或门牌就停止 |
| `ph-source-grade` | 按行内已有来源分级 |
| `ph-vector-signal` | 人群事件和病媒密度分开 |
| `ph-respiratory-week` | 阳性率不写成发病率，病原不相加 |
| `ph-cluster-notes` | 记录聚集性事件里已经给出的字段 |

## 中文社区技能

[`COMMUNITY.md`](COMMUNITY.md) 列出另外 65 个面向中文办公、校园和 WorkBuddy 使用场景的技能。来源是 [po-et/workbuddy-skills](https://github.com/po-et/workbuddy-skills)，作者 Captain。每个技能单独一个 zip，放在 `packages/`。

## 许可

新写的技能说明为 MIT。`minimax-code-trajectory` 与 `hello-mcode` 保持 Apache-2.0，版权归原作者。社区技能的正文是 CC BY 4.0，代码是 MIT，版权归 Captain。
