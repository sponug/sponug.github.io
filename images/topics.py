"""
topics.py

Generate human-readable ranked topics from your ingested annual reports in ChromaDB.
"""

from chromadb import PersistentClient
from sklearn.cluster import KMeans
import numpy as np
from collections import Counter
from openai import OpenAI

# === CONFIG ===
DB_FOLDER = "rag_db"
COLLECTION_NAME = "annual_reports"
NUM_TOPICS = 10          # number of clusters / topics
CHUNK_SAMPLE = 5         # number of chunks per cluster to summarize (avoid token overflow)
OPENAI_MODEL = "gpt-4o-mini"

# === SETUP ===
chroma_client = PersistentClient(path=DB_FOLDER)
collection = chroma_client.get_collection(COLLECTION_NAME)
client = OpenAI()  # Make sure OPENAI_API_KEY is set

# === STEP 1: Load all documents and embeddings ===
docs = collection.get(include=["documents", "embeddings"])
texts = docs["documents"]
embeddings = np.array(docs["embeddings"], dtype=np.float32)

# Filter out invalid embeddings containing NaNs
valid_indices = [i for i, emb in enumerate(embeddings) if emb is not None and not np.isnan(emb).any()]
texts = [texts[i] for i in valid_indices]
embeddings = embeddings[valid_indices]

if not texts or len(texts) != len(embeddings):
    raise ValueError("No valid embeddings found or mismatch between documents and embeddings in ChromaDB")

# === STEP 2: Cluster embeddings ===
kmeans = KMeans(n_clusters=NUM_TOPICS, random_state=42)
labels = kmeans.fit_predict(embeddings)

clusters = {i: [] for i in range(NUM_TOPICS)}
for text, label in zip(texts, labels):
    clusters[label].append(text)

# === STEP 3: Generate human-readable labels using GPT ===
cluster_labels = {}

for cluster_id, cluster_texts in clusters.items():
    # Take first few chunks to avoid token overflow
    sample_text = "\n\n".join(t[:1500] for t in cluster_texts[:CHUNK_SAMPLE])
    
    prompt = f"""
You are a financial analyst. Read the following excerpts from annual reports.
Summarize the main topic of these excerpts in 3-5 words as a human-readable label.

Text:
{sample_text}
"""
    
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        label = response.choices[0].message.content.strip()
    except Exception as e:
        label = f"Cluster_{cluster_id}"  # fallback
        print(f"❌ GPT label generation failed for cluster {cluster_id}: {e}")
    
    cluster_labels[cluster_id] = label

# === STEP 4: Rank topics by frequency ===
label_counts = Counter([cluster_labels[label] for label in labels])

print("\n=== Ranked Main Topics Across All Annual Reports ===\n")
for rank, (topic, count) in enumerate(label_counts.most_common(), start=1):
    print(f"{rank}. {topic} ({count} chunks)")

print("\n✅ Human-readable topics generated successfully.")
