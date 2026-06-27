# 老麦商业 IP 智能体

这是一个面向“老麦商业 IP 内容系统”的最小可运行 RAG 项目。它支持导入 Markdown 知识库、按标题结构语义切片、按意图路由检索资料，并用不同输出模式生成选题、脚本、朋友圈、销售话术、SOP 回答和会议投喂资料。

## 技术方案

- 后端：Python FastAPI
- 前端：单页 HTML，无构建步骤
- 知识库：`knowledge/` 中的 Markdown 文件
- 投喂源：默认支持从 `私董会学员ai投喂资料/` 批量导入
- 检索：本地 Hash 向量 + 关键词混合检索
- LLM：可选 OpenAI API；未配置时返回带来源的结构化草稿

## 快速开始

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python scripts\ingest.py --source "私董会学员ai投喂资料"
uvicorn app.main:app --reload
```

浏览器打开：<http://127.0.0.1:8000>

## 常用命令

批量导入资料：

```powershell
python scripts\ingest.py --source "私董会学员ai投喂资料"
```

运行基础测试：

```powershell
python -m pytest
```

## 知识库目录

```text
knowledge/
  01_persona/
  02_original_quotes/
  03_meeting_summaries/
  04_company/
  05_products/
  06_cases/
  07_sop/
  08_sales_faq/
  09_prompts/
  10_evaluation/
```

## 示例问题

1. 帮我生成 10 个适合老板 IP 的小红书选题，主题是低成本获客。
2. 把蓝V体系整理成一条 60 秒短视频口播脚本。
3. 客户说“我现在没预算”，给我一套私聊回复话术。
4. 蓝V内容生产前，客户资料必须交付哪些内容？
5. 用老麦风格讲清楚：为什么平台只是切口，商业才是主线？

## 来源与边界

每次回答都会尽量列出来源文件和章节。当前知识库找不到明确案例或数据时，系统会标注“基于已有方法论推导，建议人工确认”。

如果 Markdown 在界面中出现乱码，请优先用 UTF-8 重新导出原文件。本项目导入器会尝试 UTF-8、UTF-8 BOM、GB18030 等编码，但无法完全修复已经被错误转码的文本。
