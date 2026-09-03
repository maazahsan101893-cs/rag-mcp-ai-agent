# 🤖 RAG MCP FastAPI AI Assistant

An intelligent AI assistant built with **FastAPI, LangChain, Model Context Protocol (MCP), Google Gemini, RAG, ChromaDB, and web search**.

The system intelligently routes each user query to the appropriate MCP tool:

* 📚 **RAG Search** → Questions about the HEC Generative AI Training Program
* 🧠 **General Search** → Stable general-knowledge questions
* 🌐 **Web Search** → Current and internet-dependent information

The entire application is containerized using **Docker** and can be deployed to cloud platforms such as Render.

---

## 🏗️ Architecture

```text
                        User
                         │
                         ▼
                  ┌─────────────┐
                  │   FastAPI   │
                  │   /query    │
                  └──────┬──────┘
                         │
                         ▼
                ┌─────────────────┐
                │ LangChain Agent │
                │   AI Router     │
                └────────┬────────┘
                         │
              MCP Client │
                         ▼
              ┌────────────────────┐
              │    MCP Server      │
              │    rag_server.py   │
              └─────────┬──────────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
   ┌────────────┐ ┌────────────┐ ┌────────────┐
   │ search_rag │ │search_     │ │ search_web │
   │            │ │general     │ │            │
   └─────┬──────┘ └─────┬──────┘ └─────┬──────┘
         │              │              │
         ▼              ▼              ▼
    ChromaDB         Gemini        DuckDuckGo
    + Gemini         Gemini        + Gemini
    Embeddings
```

---

## ✨ Features

### 📚 Retrieval-Augmented Generation

The application loads the HEC Generative AI Training Program PDF and creates a searchable vector database.

Pipeline:

```text
PDF
 ↓
Document Loader
 ↓
Text Splitting
 ↓
Gemini Embeddings
 ↓
ChromaDB
 ↓
Retriever
 ↓
Relevant Context
 ↓
Gemini
 ↓
Answer
```

The PDF is split using:

```text
chunk_size = 1000
chunk_overlap = 200
```

---

### 🧠 Intelligent Query Routing

The LangChain agent determines which MCP tool should handle the user's question.

| Query Type                     | MCP Tool         |
| ------------------------------ | ---------------- |
| HEC Generative AI Training PDF | `search_rag`     |
| Stable general knowledge       | `search_general` |
| Current/internet information   | `search_web`     |

Examples:

```text
"What is Week 1 of the HEC Generative AI program?"
        ↓
search_rag
```

```text
"What is recursion in Python?"
        ↓
search_general
```

```text
"What is the current USD to PKR rate?"
        ↓
search_web
```

---

## 🔌 MCP Tools

The project uses **FastMCP** to expose the application's capabilities as MCP tools.

### `search_rag`

Used for questions related to the HEC Generative AI Training Program PDF.

```python
search_rag(question: str)
```

Uses:

* PyPDFLoader
* RecursiveCharacterTextSplitter
* Google Gemini Embeddings
* ChromaDB
* Gemini

---

### `search_general`

Used for stable general-knowledge questions.

```python
search_general(question: str)
```

Examples:

* What is Python?
* What is recursion?
* What is OOP?
* What is an API?

---

### `search_web`

Used for information that depends on the internet or may change over time.

```python
search_web(question: str)
```

Uses:

* DuckDuckGo Search
* Google Gemini

Examples:

* Current prices
* Recent news
* Latest AI developments
* Current software information
* Current events

---

# 🛠️ Technology Stack

| Technology        | Purpose                     |
| ----------------- | --------------------------- |
| Python            | Programming language        |
| FastAPI           | REST API                    |
| LangChain         | Agent and LLM orchestration |
| FastMCP           | MCP server                  |
| MCP Adapters      | MCP client integration      |
| Google Gemini     | LLM                         |
| Gemini Embeddings | Vector embeddings           |
| ChromaDB          | Vector database             |
| PyPDF             | PDF processing              |
| DuckDuckGo        | Web search                  |
| Docker            | Containerization            |
| Uvicorn           | ASGI server                 |
| Pydantic          | Request validation          |

---

# 📁 Project Structure

```text
Rag_LangChain/
│
├── documents/
│   └── curriculum.pdf
│
├── main.py
├── rag_server.py
├── request.py
├── test_gemini.py
│
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
│
└── README.md
```

### `main.py`

Contains the FastAPI application and LangChain agent.

Responsibilities:

* Creates the FastAPI server
* Creates the MCP client
* Connects to the MCP server
* Discovers MCP tools
* Creates the LangChain agent
* Routes user queries
* Returns the final response

---

### `rag_server.py`

Contains the FastMCP server.

Responsibilities:

* Loads the curriculum PDF
* Splits documents into chunks
* Creates embeddings
* Creates the Chroma vector store
* Creates the retriever
* Defines MCP tools
* Handles RAG, general, and web searches

---

### `documents/curriculum.pdf`

The knowledge source used by the RAG pipeline.

---

### `Dockerfile`

Defines the production container used to run the application.

---

# 🚀 Local Setup

## 1. Clone the repository

```bash
git clone https://github.com/maazahsan101893-cs/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace `YOUR_REPOSITORY` with your actual repository name.

---

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

---

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

⚠️ **Never commit `.env` to GitHub.**

The project already includes `.env` in `.gitignore`.

---

# ▶️ Run the Application

Start FastAPI with:

```powershell
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# 📡 API Usage

## Endpoint

```http
POST /query
```

### Request

```json
{
  "query": "What is HEC Generative AI training?"
}
```

### Example using PowerShell

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/query" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"query":"What is HEC Generative AI training?"}'
```

### Example response

```json
{
  "answer": "The HEC Generative AI Training Program ..."
}
```

---

# 🐳 Running with Docker

Build the Docker image:

```powershell
docker build -t rag-mcp-api .
```

Run the container:

```powershell
docker run --rm -p 10000:10000 --env-file .env rag-mcp-api
```

The API will then be available at:

```text
http://localhost:10000
```

---

## 🐳 Docker Architecture

```text
Docker Container
│
├── FastAPI
│
├── LangChain Agent
│
├── MCP Client
│
└── MCP Server
     │
     ├── RAG
     ├── General AI
     └── Web Search
```

The container receives the Gemini API key through the environment:

```text
.env
 ↓
Docker
 ↓
Environment Variable
 ↓
FastAPI / MCP Server
 ↓
Gemini
```

The `.env` file is **not copied into the Docker image** because it is excluded through `.dockerignore`.

---

# 🔐 Environment Variables

The application requires:

| Variable         | Description           |
| ---------------- | --------------------- |
| `GOOGLE_API_KEY` | Google Gemini API key |

Example:

```env
GOOGLE_API_KEY=your_api_key_here
```

Never expose your API key publicly.

---

# 🧪 Testing

The project can be tested locally through the FastAPI endpoint.

Example questions:

### RAG

```text
What is the HEC Generative AI Training Program?
```

```text
What topics are covered in the program?
```

### General

```text
What is recursion?
```

```text
What is object-oriented programming?
```

### Web

```text
What is the current USD to PKR price?
```

---

# 📊 Query Flow

For every user question, the agent follows this routing strategy:

```text
                    User Question
                          │
                          ▼
                  LangChain Agent
                          │
             ┌────────────┼────────────┐
             │            │            │
             ▼            ▼            ▼
          HEC PDF      Stable       Current /
          question     knowledge    Internet
             │            │            │
             ▼            ▼            ▼
        search_rag   search_general search_web
             │            │            │
             └────────────┼────────────┘
                          │
                          ▼
                     Final Answer
```

---

# ⚡ Important Design Decision

The system separates **tool selection** from **tool execution** using MCP.

Instead of putting all capabilities directly inside the FastAPI application:

```text
FastAPI
   ↓
LangChain
   ↓
Everything
```

the application uses:

```text
FastAPI
   ↓
LangChain Agent
   ↓
MCP Client
   ↓
MCP Server
   ↓
Specialized Tools
```

This makes the architecture more modular and allows additional tools to be added without significantly changing the main application.

---

# 🔮 Future Improvements

Potential improvements include:

* [ ] Persistent ChromaDB storage
* [ ] Conversation memory
* [ ] Streaming responses
* [ ] Authentication
* [ ] Rate-limit handling
* [ ] Better web-search pipeline
* [ ] Automated tests
* [ ] CI/CD with GitHub Actions
* [ ] Deployment to Render
* [ ] GitHub Container Registry
* [ ] Observability and logging
* [ ] More MCP tools
* [ ] Multi-document RAG
* [ ] Metadata filtering
* [ ] Hybrid search
* [ ] Reranking

---

# ⚠️ Current Limitations

The application depends on external Gemini API access.

If the Gemini API quota is exceeded, requests can fail with a `429 RESOURCE_EXHAUSTED` error.

The web-search functionality also depends on external search availability.

---

# 👨‍💻 Author

**Maaz Ahsan**

BSCIS Student
Pakistan Institute of Engineering and Applied Sciences (PIEAS)

Interested in:

* Artificial Intelligence
* Machine Learning
* Generative AI
* RAG
* LangChain
* MCP
* FastAPI
* Backend Development

---

# 📄 License

This project is intended for educational and experimental purposes.

You may modify and extend it for your own learning and projects.
