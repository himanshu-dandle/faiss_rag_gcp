import sqlite3

# ✅ Connect to SQLite Database
conn = sqlite3.connect("llm_knowledge.db")
cursor = conn.cursor()

# ✅ Create `documents` Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT
)
""")

# ✅ Insert Sample Data
documents = [
    "FAISS is a library for efficient similarity search.",
    "LangChain helps build LLM-powered applications.",
    "Retrieval-Augmented Generation (RAG) improves LLM responses.",
    "OpenAI released GPT-4 in 2023."
]

for doc in documents:
    cursor.execute("INSERT INTO documents (content) VALUES (?)", (doc,))
conn.commit()

print("✅ SQLite Database Initialized with Sample Data!")
