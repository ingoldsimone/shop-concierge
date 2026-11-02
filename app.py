"""Shopping concierge: a tiny RAG + tool-calling API.

With OPENAI_API_KEY set -> OpenAI embeddings + chat with tool-calling.
Without it            -> offline demo mode (TF-IDF retrieval, rule-based tool use).
"""
import json
import os

import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

load_dotenv()  # reads .env into environment variables (optional)

DOCS = json.load(open(os.path.join(os.path.dirname(__file__), "docs.json")))
TEXTS = [f"{d['title']}. {d['text']}" for d in DOCS]
USE_OPENAI = bool(os.getenv("OPENAI_API_KEY"))
TOP_K = 3
DEMO_MIN_SCORE = 0.12  # below this, demo mode says "I don't know"

# ---- Tool: a fake store-discount lookup the LLM can call ----
STORES = {
    "nimbus outdoors": {"discount": "20%", "groups": ["military", "students"]},
    "brightside shoes": {"discount": "15%", "groups": ["nurses", "teachers", "first responders"]},
    "pixel parts": {"discount": "10%", "groups": ["students"]},
}


def get_discount(store: str) -> dict:
    info = STORES.get(store.strip().lower())
    return {"store": store, **info} if info else {"store": store, "error": "store not found"}


def find_stores(group: str) -> dict:
    g = group.strip().lower()
    return {
        "group": group,
        "stores": [n.title() for n, i in STORES.items() if any(g in x or x in g for x in i["groups"])],
    }


TOOL_FUNCS = {"get_discount": get_discount, "find_stores": find_stores}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_discount",
            "description": "Look up the member discount and eligible groups for a store.",
            "parameters": {
                "type": "object",
                "properties": {"store": {"type": "string"}},
                "required": ["store"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_stores",
            "description": "List stores that offer discounts to a group (e.g. nurses, students).",
            "parameters": {
                "type": "object",
                "properties": {"group": {"type": "string"}},
                "required": ["group"],
            },
        },
    },
]

# ---- Embeddings: pick a backend, then retrieval is the same either way ----
if USE_OPENAI:
    from openai import OpenAI

    client = OpenAI()

    def embed(texts):
        r = client.embeddings.create(model="text-embedding-3-small", input=texts)
        return np.array([d.embedding for d in r.data])
else:
    from sklearn.feature_extraction.text import TfidfVectorizer

    _vec = TfidfVectorizer(stop_words="english").fit(TEXTS)

    def embed(texts):
        return _vec.transform(texts).toarray()


def _normalize(m):
    n = np.linalg.norm(m, axis=1, keepdims=True)
    return m / np.where(n == 0, 1, n)


DOC_VECS = _normalize(embed(TEXTS))  # embedded once at startup, kept in memory


def retrieve(question: str, k: int = TOP_K):
    q = _normalize(embed([question]))[0]
    scores = DOC_VECS @ q  # cosine similarity (vectors are unit length)
    top = np.argsort(scores)[::-1][:k]
    return [(DOCS[i], float(scores[i])) for i in top]


# ---- Answering ----
SYSTEM = (
    "You are a shopping concierge. Answer ONLY using the provided context or the "
    "tools (get_discount, find_stores). Do not add claims, guarantees, or details "
    "that are not in the context. If the answer is not there, say you don't know "
    "and suggest contacting support. Be brief."
)


def answer_openai(question, hits):
    context = "\n\n".join(f"[{d['id']}] {d['text']}" for d, _ in hits)
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ]
    tools_used = []
    for _ in range(3):  # allow a few tool-call rounds
        msg = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages, tools=TOOLS
        ).choices[0].message
        if not msg.tool_calls:
            return msg.content, tools_used
        messages.append(msg)
        for call in msg.tool_calls:
            result = TOOL_FUNCS[call.function.name](**json.loads(call.function.arguments))
            tools_used.append({"name": call.function.name, "result": result})
            messages.append(
                {"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)}
            )
    return "Sorry, I couldn't finish that request.", tools_used


def answer_demo(question, hits):
    q = question.lower()
    for name in STORES:  # rule-based stand-in for LLM tool-calling
        if name in q:
            r = get_discount(name)
            text = f"{name.title()} offers {r['discount']} off for: {', '.join(r['groups'])}."
            return text, [{"name": "get_discount", "result": r}]
    best_doc, best_score = hits[0]
    if best_score < DEMO_MIN_SCORE:
        return "I don't know. Please contact support.", []
    return best_doc["text"], []


# ---- API ----
app = FastAPI(title="Shopping Concierge")


class Ask(BaseModel):
    question: str


@app.post("/ask")
def ask(body: Ask):
    hits = retrieve(body.question)
    answer, tools = (answer_openai if USE_OPENAI else answer_demo)(body.question, hits)
    return {
        "answer": answer,
        "sources": [d["id"] for d, _ in hits],
        "tools_used": tools,
        "mode": "openai" if USE_OPENAI else "demo",
    }


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "index.html"))


@app.get("/health")
def health():
    return {"status": "ok", "mode": "openai" if USE_OPENAI else "demo"}
