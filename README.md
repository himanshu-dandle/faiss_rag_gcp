#  FAISS RAG API - FastAPI + FAISS + OpenAI + GCP Cloud Run

This project implements a **Retrieval-Augmented Generation (RAG) API** using **FAISS for similarity search** and **FastAPI** for serving search queries. The API is deployed on **Google Cloud Run**, making it scalable and accessible via HTTP requests.

---

## 🔹 **Project Features**
1. **FAISS-based Vector Search** - Efficient similarity search using OpenAI embeddings.  
2. **FastAPI Backend** - Lightweight and high-performance API server.  
3. **Google Cloud Run Deployment** - Serverless deployment for global accessibility.  
4. **Retrieval-Augmented Generation (RAG) Integration** - Combines FAISS search results with LLMs.  
5. **Docker Containerization** - Runs in an isolated environment for easy deployment.  

---

##  **Project Structure**
```
FAISS_RAG_GCP/
│
├── .env                      # Environment variables (ignored in .gitignore)
├── .gitignore                 # Files & folders to ignore in Git
├── api/                       # API-related code (if needed)
├── build_faiss_index.py       # Script to build FAISS index
├── Dockerfile                 # Docker container setup
├── faiss_index/               # FAISS index storage (ignored in .gitignore)
├── gcp_deployment/            # Cloud Run deployment configs
├── initialize_db.py           # Initializes SQLite DB
├── LICENSE                    # License file
├── llm_knowledge.db           # SQLite database (ignored in .gitignore)
├── main.py                    # FastAPI main application
├── README.md                  # Project documentation
├── requirements.txt           # Project dependencies
├── tests/                     # Unit tests (currently empty)
├── utils/                     # Utility functions
├── venv/                      # Virtual environment (ignored in .gitignore)
└── __pycache__/               # Compiled Python files (ignored in .gitignore)
```
---

##  **Setup & Installation**

### **🔹 Step 1: Clone the Repository**

git clone https://github.com/himanshu-dandle/faiss_rag_gcp.git
cd faiss_rag_gcp


### **🔹 Step 2: Create a Virtual Environment & Install Dependencies**

	python -m venv venv
	source venv/bin/activate  # On Mac/Linux
	venv\Scripts\activate     # On Windows

	pip install -r requirements.txt
	

### **🔹 Step 3: Set Up Environment Variables**
	Create a .env file in the project root and add your OpenAI API Key:
	
		OPENAI_API_KEY=your_openai_api_key_here



### **🔹 Step 4: Initialize Database & Build FAISS Index**

	python initialize_db.py
	python build_faiss_index.py

### **🔹 Step 5: Run the FastAPI Server Locally**

		uvicorn main:app --host 0.0.0.0 --port 8000
	Now, visit: http://127.0.0.1:8000/docs to test the API.
	


##  **Deployment on Google Cloud Run**
	The API is deployed using Docker & Google Cloud Run.

	🔹 Step 1: Build & Push Docker Image
		docker build -t gcr.io/faiss-rag-gcp/faiss-rag-api .
		docker push gcr.io/faiss-rag-gcp/faiss-rag-api
	🔹 Step 2: Deploy to Cloud Run
		gcloud run deploy faiss-rag-api ^
			--image gcr.io/faiss-rag-gcp/faiss-rag-api ^
			--platform managed ^
			--region us-central1 ^
			--allow-unauthenticated
			
	Your API will be live at: https://faiss-rag-api-xxxxxx.a.run.app



## **How to Use the API**
### **🔹 API Endpoint: POST /search**
	1. Sends a query to the FAISS-powered retrieval system.
	2. Returns the most relevant documents.
		 Example Request
			curl -X POST "https://faiss-rag-api-xxxxxx.a.run.app/search" ^
				 -H "Content-Type: application/json" ^
				 -d "{\"query\": \"What is FAISS?\"}"
		 Example Response
			{
				"query": "What is FAISS?",
				"retrieved_docs": [
					"FAISS is a library for efficient similarity search.",
					"Retrieval-Augmented Generation (RAG) improves LLM responses.",
					"OpenAI released GPT-4 in 2023."
				]
			}
**How FAISS Works**
1. FAISS stores vector embeddings of documents.
2. User queries are converted into embeddings using OpenAI embeddings.
3. FAISS performs a nearest-neighbor search to find the closest documents.
4. The API returns the most relevant documents based on similarity scores.

**Next Steps & Enhancements**
1. Integrate an LLM (e.g., GPT-4) to generate contextual answers.
2. Use Google’s Vertex AI Matching Engine for a more scalable solution.
3. Build a UI using Streamlit or Gradio for an interactive chatbot.

Author: Himanshu Dandle
GitHub: https://github.com/himanshu-dandle
