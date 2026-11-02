"""Run sample questions through the API and save the answers to samples_<mode>.md.

  python record_samples.py                          # demo mode (no key)
  OPENAI_API_KEY=sk-... python record_samples.py    # openai mode

"""
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
    "Which store has discounts for nurses?",   # needs reasoning over the tool data
    "What's the weather in Paris?",            # out of scope, should refuse
    "Write me a poem about cats",              # out of scope, should refuse
]

client = TestClient(app)
out, mode = [], None
for q in QUESTIONS:
    r = client.post("/ask", json={"question": q}).json()
    mode = r["mode"]
    out.append(f"### {q}\n\n{r['answer']}\n\n- Retrieved: {', '.join(r['sources'])}")
    for t in r["tools_used"]:
        out[-1] += f"\n- Tool call: `{t['name']}` -> `{t['result']}`"
    print("done:", q)

path = f"samples_{mode}.md"
with open(path, "w") as f:
    f.write(f"# Sample responses ({mode} mode)\n\n" + "\n\n".join(out) + "\n")
print("wrote", path)
