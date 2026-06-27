from __future__ import annotations

from app.rag.config import ENABLE_OPENAI_GENERATION, OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL

MODE_TITLES = {
    "topics": "选题建议",
    "script": "短视频口播脚本",
    "moments": "朋友圈内容",
    "sales": "销售私聊话术",
    "sop": "SOP 回答",
    "meeting_to_knowledge": "会议投喂资料",
}


def build_prompt(query: str, mode: str, sources: list[dict], system_prompt: str) -> str:
    context = "\n\n".join(
        f"[{idx}] {item['chunk']['file_path']} > {item['chunk']['section_path']}\n{item['chunk']['content']}"
        for idx, item in enumerate(sources, start=1)
    )
    return f"""{system_prompt}

用户问题：
{query}

输出模式：{mode}

可参考资料：
{context}

要求：
1. 只基于参考资料和可推导的方法论回答。
2. 不虚构案例、数据和老麦原话。
3. 结尾必须列出“参考来源”。
4. 如果资料没有明确依据，必须说明需要人工确认。
"""


def generate_answer(query: str, mode: str, sources: list[dict], system_prompt: str) -> str:
    if ENABLE_OPENAI_GENERATION and OPENAI_API_KEY:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": build_prompt(query, mode, sources, system_prompt)},
                ],
                temperature=0.4,
            )
            return response.choices[0].message.content or ""
        except Exception as exc:
            return _fallback_answer(query, mode, sources, f"LLM 调用失败：{exc}")
    return _fallback_answer(query, mode, sources)


def _fallback_answer(query: str, mode: str, sources: list[dict], note: str | None = None) -> str:
    title = MODE_TITLES.get(mode, mode)
    evidence = "\n\n".join(
        f"- {item['chunk']['section_path']}：{item['chunk']['content'][:220].strip()}..."
        for item in sources[:4]
    )
    source_lines = "\n".join(
        f"- {item['chunk']['file_path']} > {item['chunk']['section_path']}"
        for item in sources[:6]
    )
    caveat = note or "当前未配置 OpenAI API，以下为基于检索资料生成的结构化草稿，建议人工润色确认。"
    return f"""# {title}

## 前置判断
- 用户需求：{query}
- 生成依据：优先使用检索到的老麦方法论、SOP、产品/销售资料。
- 风险提示：{caveat}

## 可用素材
{evidence or "- 当前知识库没有找到足够明确的素材。"}

## 初版输出
当前知识库已找到相关资料。请基于上面的素材组织成“判断先行、观点明确、可执行、有承接”的老麦商业 IP 内容。不要把 SOP 或公司介绍写成老麦亲口说过的话。

## 参考来源
{source_lines or "- 当前知识库没有找到明确来源。"}
"""
