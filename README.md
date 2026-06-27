# 老麦商业 IP Skill

这是一个可安装到 Codex 的「老麦商业 IP」Skill 包。它把老麦商业 IP 内容生产流程、输出模板、会议整理方法和内置投喂资料打包在一起，让 Codex 可以按固定工作流生成选题、脚本、朋友圈、销售话术、SOP 回答和会议投喂资料。

## Skill 位置

```text
skills/laomai-business-ip
```

## Skill 包含什么

- `SKILL.md`：老麦商业 IP 工作流规则
- `agents/openai.yaml`：Codex Skill 展示信息
- `references/output-formats.md`：选题、脚本、朋友圈、销售、SOP 等输出格式
- `references/meeting-to-knowledge.md`：会议记录整理成投喂资料的流程
- `references/knowledge/`：内置投喂资料
- `references/knowledge/knowledge-index.md`：内置资料索引

## 安装方式

在 Codex 中可以直接说：

```text
安装这个 Skill：jasonwong363/laomai-business-ip-agent，路径 skills/laomai-business-ip
```

也可以使用安装脚本：

```powershell
python C:\Users\jason\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py --repo jasonwong363/laomai-business-ip-agent --path skills/laomai-business-ip
```

安装后重启 Codex。

## 使用方式

```text
用 $laomai-business-ip，基于内置资料生成 10 个低成本获客选题，并标注来源。
```

```text
用 $laomai-business-ip，把会议记录整理成老麦智能体投喂资料和老麦原话精选语料库。
```

```text
用 $laomai-business-ip，基于内置资料写一套客户说“没预算”的销售私聊话术。
```

## 它适合做什么

- 会议记录整理成智能体投喂资料
- 老麦原话和方法论沉淀
- 生成商业 IP 选题
- 生成短视频口播脚本
- 生成朋友圈和私域内容
- 生成销售私聊话术
- 回答蓝V、KOC、内容矩阵相关 SOP 问题
- 拆解案例和提炼可复用方法论

## 工作边界

这个 Skill 会尽量基于内置资料和用户提供资料回答。没有明确案例或数据时，应该标注：

```text
当前知识库没有找到明确案例或数据，以下为基于已有方法论的推导，建议人工确认。
```

不要虚构案例、数据、客户结果、老麦原话或产品保证。
