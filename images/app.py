# app_bmc_query.py

import os
import streamlit as st
import numpy as np
from openai import OpenAI
import chromadb
from chromadb.config import Settings

# ================== CONFIG ==================
DB_DIR = "rag_db"
COLLECTION_NAME = "annual_reports"
YEARS_TO_INCLUDE = list(range(2013, 2023))  # last 10 fiscal years
EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o"
TOP_K = 6  # chunks retrieved per query

BMC_BLOCKS = [
    "Customer Segments", "Value Propositions", "Channels",
    "Customer Relationships", "Revenue Streams", "Key Resources",
    "Key Activities", "Key Partnerships", "Cost Structure"
]

BMC_QUESTIONS = {
    "Customer Segments": [
        "Who are the main customer segments and how do they contribute to revenue in the last 10 years?",
        "Describe target markets by region or industry over the last 10 years."
    ],
    "Value Propositions": [
        "Summarize the company's key products/services and unique value propositions from the last 10 years.",
        "What competitive advantages or moats are highlighted in this period?"
    ],
    "Channels": [
        "Through which channels did the company reach its customers in the last 10 years?",
        "Describe distribution, sales, and marketing channels in the last 10 years."
    ],
    "Customer Relationships": [
        "How did the company maintain and engage customer relationships over the last 10 years?",
        "Are there loyalty programs or service agreements mentioned in this period?"
    ],
    "Revenue Streams": [
        "Provide the main sources of revenue and their splits over the last 10 years.",
        "Include recurring vs one-time revenues where mentioned."
    ],
    "Key Resources": [
        "List the key assets the company relied on in the last 10 years (physical, intellectual, human, tech)."
    ],
    "Key Activities": [
        "What were the core activities to deliver the company's products/services in the last 10 years?",
        "Include operations, R&D, production, marketing, or service delivery."
    ],
    "Key Partnerships": [
        "List strategic partners, suppliers, and alliances and their roles in the last 10 years."
    ],
    "Cost Structure": [
        "Summarize the main costs and expenditures of the company over the last 10 years.",
        "Include major operational or capital expenses."
    ]
}

# ================== STREAMLIT SETUP ==================
st.set_page_config(page_title="Business Canvas Query", layout="wide")
st.title("📊 Business Model Canvas – Westpac(10 Years)")

with st.sidebar:
    st.header("Settings")
    chat_model = st.text_input("Chat Model", value=CHAT_MODEL)
    embed_model = st.text_input("Embedding Model", value=EMBED_MODEL)
    top_k = st.slider("Top-K passages to retrieve", min_value=3, max_value=12, value=TOP_K)
    if st.button("Reset DB (Danger!)"):
        import shutil
        shutil.rmtree(DB_DIR, ignore_errors=True)
        st.success("Deleted DB folder. Restart to re-create.")

# ================== OPENAI & CHROMADB ==================
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OPENAI_API_KEY not set. Please set it and restart.")
        st.stop()
    return OpenAI()

client = get_openai_client()

def get_chroma_collection():
    chroma_client = chromadb.PersistentClient(path=DB_DIR, settings=Settings(allow_reset=False))
    try:
        col = chroma_client.get_or_create_collection(name=COLLECTION_NAME)
    except TypeError:
        col = chroma_client.get_or_create_collection(name=COLLECTION_NAME)
    return col

collection = get_chroma_collection()

# ================== RETRIEVAL & GPT ==================
def compute_embedding(text):
    resp = client.embeddings.create(model=embed_model, input=text)
    emb = resp.data[0].embedding
    if emb is None or any(np.isnan(emb)):
        raise ValueError("Embedding returned NaN or None")
    return emb

def retrieve(query, top_k=TOP_K):
    year_filter = " OR ".join(str(y) for y in YEARS_TO_INCLUDE)
    query_with_years = f"{query}. Only include data mentioning these years: {year_filter}"
    q_emb = compute_embedding(query_with_years)
    res = collection.query(
        query_embeddings=[q_emb],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]
    return list(zip(docs, metas, dists))

def summarize_with_gpt(query, retrieved_chunks):
    if not retrieved_chunks:
        return "No relevant information found."
    context = ""
    for i, (doc, meta, dist) in enumerate(retrieved_chunks, start=1):
        tag = f"[S{i} {meta.get('source')} p.{meta.get('page')}]"
        context += f"{tag}\n{doc[:1500]}\n\n"
    prompt = f"""
You are a meticulous business analyst. Answer the question below using ONLY the context provided.
Focus strictly on the last 10 fiscal years ({YEARS_TO_INCLUDE[0]}–{YEARS_TO_INCLUDE[-1]}).
Cite sources inline using the [S#] tags.

Question: {query}

Context:
{context}
"""
    resp = client.chat.completions.create(
        model=chat_model,
        messages=[{"role":"user","content":prompt}],
        temperature=0.2
    )
    return resp.choices[0].message.content.strip()

# ================== FREEFORM QUERY ==================
st.subheader("Ask a Question Across All Annual Reports")
user_query = st.text_input("Enter your question", placeholder="e.g., What are the main business segments and revenue trends?")
if st.button("Get Answer"):
    if not user_query.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Retrieving relevant content and generating answer..."):
            retrieved = retrieve(user_query, top_k=top_k)
            answer = summarize_with_gpt(user_query, retrieved)
        st.markdown("### Answer")
        st.write(answer)
        st.markdown("### Sources")
        for i, (doc, meta, dist) in enumerate(retrieved, start=1):
            with st.expander(f"[S{i}] {meta.get('source')} – page {meta.get('page')} (similarity: {1 - dist:.3f})"):
                st.write(doc)

