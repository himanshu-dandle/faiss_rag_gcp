import os
import faiss
import numpy as np
import sqlite3
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# ✅ Load .env File (Force Reload)
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# ✅ Manually Set API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not found! Please check .env file or set manually.")

# ✅ Ensure `faiss_index/` directory exists
faiss_index_path = "faiss_index/sql_faiss.index"
os.makedirs("faiss_index", exist_ok=True)

# ✅ Load SQLite Data
conn = sqlite3.connect("llm_knowledge.db")
cursor = conn.cursor()
cursor.execute("SELECT content FROM documents")
rows = cursor.fetchall()
sql_documents = [row[0] for row in rows]

if not sql_documents:
    raise ValueError("❌ No documents found in SQLite database. Please insert data first!")

# ✅ Generate Embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)  # ✅ Fix: Pass API key explicitly
doc_embeddings = [embeddings.embed_query(doc) for doc in sql_documents]
doc_embeddings = np.array(doc_embeddings, dtype=np.float32)

# ✅ Create FAISS Index
d = 1536  # OpenAI Embedding size
index = faiss.IndexFlatL2(d)
index.add(doc_embeddings)

# ✅ Save FAISS Index
faiss.write_index(index, faiss_index_path)
print(f"✅ FAISS Index Created and Saved at: {faiss_index_path}")
