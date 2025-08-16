import os
import glob
import uuid
import time
from pypdf import PdfReader
from chromadb import PersistentClient
from openai import OpenAI

# === CONFIG ===
PDF_FOLDER = "annual_reports"   # folder containing your PDFs
DB_FOLDER = "rag_db"            # persistent Chroma database
CHUNK_SIZE = 500                # number of characters per chunk
CHUNK_OVERLAP = 50              # overlap between chunks
COLLECTION_NAME = "annual_reports"
ERROR_LOG = "error.txt"
EMBED_BATCH_SIZE = 50           # number of chunks per embedding request

# === SETUP ===
os.makedirs(DB_FOLDER, exist_ok=True)
chroma_client = PersistentClient(path=DB_FOLDER)
collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)
client = OpenAI()  # Make sure OPENAI_API_KEY is set in your environment

# ---------------- Functions ----------------

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def embed_text(texts, batch_size=EMBED_BATCH_SIZE):
    """Generate embeddings safely in batches."""
    # Remove empty or non-string entries
    clean_texts = [t for t in texts if isinstance(t, str) and t.strip()]
    if not clean_texts:
        return []

    embeddings = []
    for i in range(0, len(clean_texts), batch_size):
        batch = clean_texts[i:i+batch_size]
        if not batch:
            continue
        try:
            resp = client.embeddings.create(
                model="text-embedding-3-small",
                input=batch
            )
            embeddings.extend([d.embedding for d in resp.data])
        except Exception as e:
            print(f"❌ Embedding batch failed: {str(e)}")
            with open(ERROR_LOG, "a", encoding="utf-8") as f:
                f.write(f"Embedding batch failed: {str(e)}\n")
    return embeddings

def process_pdf(file_path):
    """Read and chunk a PDF, return chunks with metadata."""
    reader = PdfReader(file_path)
    all_chunks = []
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if not text or not text.strip():
            continue
        chunks = chunk_text(text)
        for chunk in chunks:
            metadata = {
                "source": os.path.basename(file_path),
                "page": page_num
            }
            all_chunks.append((chunk, metadata))
    return all_chunks

def ingest_pdfs():
    pdf_files = glob.glob(os.path.join(PDF_FOLDER, "*.pdf"))
    print(f"Found {len(pdf_files)} PDF(s) in {PDF_FOLDER}/")

    success_count = 0
    fail_count = 0

    # Clear old error log
    if os.path.exists(ERROR_LOG):
        os.remove(ERROR_LOG)

    for pdf in pdf_files:
        start_time = time.time()  # start timer
        try:
            print(f"📄 Processing {pdf} ...")
            chunks = process_pdf(pdf)
            if not chunks:
                print(f"⚠️ Skipped {pdf} (no text found).")
                continue

            texts, metadatas, ids = [], [], []
            for chunk, metadata in chunks:
                if isinstance(chunk, str) and chunk.strip():
                    texts.append(chunk)
                    metadatas.append(metadata)
                    ids.append(str(uuid.uuid4()))

            if not texts:
                print(f"⚠️ No valid chunks found in {pdf}")
                continue

            embeddings = embed_text(texts)

            if not embeddings or len(embeddings) != len(texts):
                print(f"⚠️ Embedding mismatch or failed for {pdf}")
                with open(ERROR_LOG, "a", encoding="utf-8") as f:
                    f.write(f"Embedding failed for {pdf}\n")
                continue

            collection.add(
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )

            elapsed = time.time() - start_time  # compute elapsed time
            print(f"✅ Finished {pdf} -> {len(texts)} chunks stored. Time taken: {elapsed:.2f} sec")
            success_count += 1

        except Exception as e:
            fail_count += 1
            error_message = f"❌ Error processing {pdf}: {str(e)}"
            print(error_message)
            with open(ERROR_LOG, "a", encoding="utf-8") as f:
                f.write(error_message + "\n")

    print("\n=== Ingestion Summary ===")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {fail_count}")
    if fail_count > 0:
        print(f"See {ERROR_LOG} for details.")

    print("\n🎉 Ingestion complete. ChromaDB is ready in", DB_FOLDER)

# ---------------- Main ----------------
if __name__ == "__main__":
    ingest_pdfs()
