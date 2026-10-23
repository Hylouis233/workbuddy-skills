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

## 中文社区技能

[`COMMUNITY.md`](COMMUNITY.md) 列出另外 65 个面向中文办公、校园和 WorkBuddy 使用场景的技能。来源是 [po-et/workbuddy-skills](https://github.com/po-et/workbuddy-skills)，作者 Captain。每个技能单独一个 zip，放在 `packages/`。

## 许可

新写的技能说明为 MIT。`minimax-code-trajectory` 与 `hello-mcode` 保持 Apache-2.0，版权归原作者。社区技能的正文是 CC BY 4.0，代码是 MIT，版权归 Captain。
