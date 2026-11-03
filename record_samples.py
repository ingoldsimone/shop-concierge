"""Run sample questions through the API and save the answers.

  python record_samples.py                          # demo mode (no key)
  OPENAI_API_KEY=sk-... python record_samples.py    # openai mode

Writes samples_<mode>.md. In openai mode it also writes docs/answers.json,
which the GitHub Pages demo replays.
"""
import json
import os

from fastapi.testclient import TestClient

from app import app

QUESTIONS = [
    "How do I verify as a student?",
    "My verification failed, what now?",
    "Can I use two coupon codes on one order?",
    "Where's my parcel?",                      # paraphrase: no keyword overlap with the doc
    "Is it safe? Will shops see my personal info?",
    "Can my spouse use my military discount?",
    "What discount does Nimbus Outdoors give?",
    "Which store has discounts for nurses?",   # needs the find_stores tool
    "What's the weather in Paris?",            # out of scope, should refuse
    "Write me a poem about cats",              # out of scope, should refuse
]

client = TestClient(app)
results, mode = [], None
for q in QUESTIONS:
    r = client.post("/ask", json={"question": q}).json()
    mode = r["mode"]
    results.append({"question": q, "answer": r["answer"],
                    "sources": r["sources"], "tools_used": r["tools_used"]})
    print("done:", q)

md = []
for x in results:
    block = f"### {x['question']}\n\n{x['answer']}\n\n- Retrieved: {', '.join(x['sources'])}"
    for t in x["tools_used"]:
        block += f"\n- Tool call: `{t['name']}` -> `{t['result']}`"
    md.append(block)

with open(f"samples_{mode}.md", "w") as f:
    f.write(f"# Sample responses ({mode} mode)\n\n" + "\n\n".join(md) + "\n")
print(f"wrote samples_{mode}.md")

if mode == "openai":
    os.makedirs("docs", exist_ok=True)
    with open("docs/answers.json", "w") as f:
        json.dump({"mode": mode, "items": results}, f, indent=2)
    print("wrote docs/answers.json")
else:
    print("skipped docs/answers.json (only written in openai mode)")
