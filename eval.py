"""Tiny eval: does retrieval find the right doc, and does it refuse out-of-scope questions?
Run: python eval.py
"""
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

# (question, expected top-3 source id, or None if it should refuse / be out of scope)
CASES = [
    ("How do I verify as a student?", "student-docs"),
    ("My verification failed, what now?", "failed"),
    ("Can I stack two coupon codes?", "stacking"),
    ("How long does shipping take?", "shipping"),
    ("Can I return a discounted item?", "returns"),
    ("Does the store see my documents?", "privacy"),
    ("Are veterans eligible?", "military"),
    ("Where is my package?", "order-status"),
    ("What discount does Nimbus Outdoors give?", "TOOL"),
    ("What's the weather in Paris?", None),
    ("Who won the 2018 World Cup?", None),
    ("Write me a poem about cats", None),
]

passed = 0
for q, expected in CASES:
    r = client.post("/ask", json={"question": q}).json()
    if expected is None:
        ok = "don't know" in r["answer"].lower()
    elif expected == "TOOL":
        ok = bool(r["tools_used"])
    else:
        ok = expected in r["sources"]
    passed += ok
    print(f"{'PASS' if ok else 'FAIL'}  [{r['mode']}] {q}")
print(f"\n{passed}/{len(CASES)} passed")
