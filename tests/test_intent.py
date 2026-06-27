from app.rag.intent import classify_intent, preferred_types


def test_classify_sales_intent() -> None:
    assert classify_intent("客户说没有预算，怎么回复", "auto") == "sales"
    assert "sales_faq" in preferred_types("sales")
