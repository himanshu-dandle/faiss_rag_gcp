import os
import faiss
import numpy as np
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI  # ✅ Use ChatOpenAI instead

# ✅ Load Environment Variables
load_dotenv()

# ✅ Initialize FastAPI
app = FastAPI()

# ✅ Load API Keys from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FAISS_INDEX_PATH = "faiss_index/sql_faiss.index"

# ✅ Load FAISS Index
if os.path.exists(FAISS_INDEX_PATH):
    index = faiss.read_index(FAISS_INDEX_PATH)
    print(f"✅ FAISS Index Loaded: {index.ntotal} documents")
else:
    raise FileNotFoundError("❌ FAISS Index not found. Please generate and save it first.")

# ✅ Load OpenAI Embeddings
embeddings = OpenAIEmbeddings()

# ✅ Load OpenAI GPT-4 Model with Chat API
llm = ChatOpenAI(model_name="gpt-4", openai_api_key=OPENAI_API_KEY)

# ✅ Define Request Model
class QueryRequest(BaseModel):
    query: str

# ✅ API Endpoint for FAISS + GPT-4 Retrieval
@app.post("/search")
def search_faiss(request: QueryRequest):
    query_embedding = np.array([embeddings.embed_query(request.query)], dtype=np.float32)
    D, I = index.search(query_embedding, k=3)  # Retrieve Top 3 Matches
    
    # ✅ Dummy Documents List (Replace with actual retrieval logic)
    documents = [
        "FAISS is a library for efficient similarity search.",
        "LangChain helps build LLM-powered applications.",
        "Retrieval-Augmented Generation (RAG) improves LLM responses.",
        "OpenAI released GPT-4 in 2023."
    ]
    
    retrieved_docs = [documents[i] for i in I[0] if i != -1]
    
    # ✅ Combine retrieved docs into a chat-based prompt for GPT-4
    messages = [
        {"role": "system", "content": "You are an AI assistant providing relevant answers based on retrieved documents."},
        {"role": "user", "content": f"Based on the following retrieved documents, answer the question:\n\n{retrieved_docs}\n\nQuestion: {request.query}"}
    ]

    # ✅ Get GPT-4 Chat Response
    response = llm.invoke(messages)

    return {
        "query": request.query,
        "retrieved_docs": retrieved_docs,
      ##  "gpt4_response": response
        "gpt4_response": response.content

    }

# ✅ Run API Locally
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Default to 8000 for local testing
    uvicorn.run(app, host="0.0.0.0", port=port)
