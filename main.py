import os
import faiss
import numpy as np
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings

#  Load Environment Variables
load_dotenv()

#  Initialize FastAPI
app = FastAPI()

#  Load API Keys from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FAISS_INDEX_PATH = "faiss_index/sql_faiss.index"

# Load FAISS Index
if os.path.exists(FAISS_INDEX_PATH):
    index = faiss.read_index(FAISS_INDEX_PATH)
    print(f"✅ FAISS Index Loaded: {index.ntotal} documents")
else:
    raise FileNotFoundError("❌ FAISS Index not found. Please generate and save it first.")

#  Load OpenAI Embeddings
embeddings = OpenAIEmbeddings()

#  Request Model
class QueryRequest(BaseModel):
    query: str

#  API Endpoint for FAISS Retrieval
@app.post("/search")
def search_faiss(request: QueryRequest):
    query_embedding = np.array([embeddings.embed_query(request.query)], dtype=np.float32)
    D, I = index.search(query_embedding, k=3)  # Retrieve Top 3 Matches
    
    # Dummy Documents List (Replace with actual document retrieval logic)
    documents = [
        "FAISS is a library for efficient similarity search.",
        "LangChain helps build LLM-powered applications.",
        "Retrieval-Augmented Generation (RAG) improves LLM responses.",
        "OpenAI released GPT-4 in 2023."
    ]
    
    retrieved_docs = [documents[i] for i in I[0] if i != -1]
    
    return {
        "query": request.query,
        "retrieved_docs": retrieved_docs
    }

#  Run API Locally
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
