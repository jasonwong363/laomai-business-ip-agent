from __future__ import annotations

INTENT_WEIGHTS: dict[str, list[str]] = {
    "topics": ["original_quotes", "meeting_summaries", "persona", "cases", "products"],
    "script": ["original_quotes", "meeting_summaries", "persona", "cases", "products"],
    "moments": ["sop", "original_quotes", "company", "products", "sales_faq"],
    "sales": ["products", "sales_faq", "cases", "original_quotes"],
    "sop": ["sop", "sales_faq", "meeting_summaries"],
    "meeting_to_knowledge": ["meeting_summaries", "original_quotes", "persona"],
    "product": ["products", "company", "sales_faq"],
    "company": ["company", "products", "cases"],
}

KEYWORDS: list[tuple[tuple[str, ...], str]] = [
    (("选题", "主题", "爆文", "内容方向"), "topics"),
    (("脚本", "口播", "短视频", "拍摄"), "script"),
    (("朋友圈", "私域"), "moments"),
    (("销售", "私聊", "异议", "成交", "话术", "客户说", "预算"), "sales"),
    (("sop", "流程", "标准", "检查清单", "执行"), "sop"),
    (("会议", "纪要", "投喂", "整理"), "meeting_to_knowledge"),
    (("产品", "课程", "陪跑", "服务"), "product"),
    (("公司", "介绍", "品牌"), "company"),
]


def classify_intent(query: str, mode: str | None = None) -> str:
    if mode and mode != "auto":
        return mode
    lowered = query.lower()
    for words, intent in KEYWORDS:
        if any(word.lower() in lowered for word in words):
            return intent
    return "topics"


def preferred_types(intent: str) -> list[str]:
    return INTENT_WEIGHTS.get(intent, ["original_quotes", "meeting_summaries", "products", "sop"])
