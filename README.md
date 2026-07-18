# DocChat 🐥 — Multi-Agent RAG for Long, Complex Documents

DocChat is a multi-agent retrieval-augmented generation (RAG) system that answers questions about long, complex documents (PDFs, Word files, text reports) with fact-checked, hallucination-resistant responses. Instead of relying on a single LLM call, DocChat orchestrates a team of specialized agents that retrieve, reason, verify, and self-correct before returning an answer.

## Why DocChat?

General-purpose chatbots often struggle with long documents that contain dense text, tables, and figures — misreading tables, missing footnoted data, or fabricating citations outright. DocChat addresses this with a structured, verification-driven pipeline instead of a single-shot LLM response.

## Key Features

- 📄 **Upload and analyze long documents** — PDFs, Word files, and text reports
- 💬 **Ask questions and get precise, source-backed answers**
- 📊 **Handle structured content** — tables, figures, and dense multi-column text
- 🚫 **Avoid hallucinations** — every answer is cross-checked against the source documents before being returned
- ⚠️ **Out-of-scope detection** — if a question can't be answered from the uploaded documents, DocChat tells you instead of guessing
- 📚 **Multi-document support** — DocChat intelligently identifies which document(s) are relevant to a given question

## How It Works

DocChat's pipeline is built around four core components:

1. **Hybrid Retriever** — combines BM25 keyword search with vector embeddings to retrieve the most relevant passages from the document store.
2. **Research Agent** — analyzes retrieved passages and drafts an initial answer.
3. **Verification Agent** — cross-checks the draft answer against the source documents to catch unsupported claims or contradictions.
4. **Self-Correction Loop** — if verification fails, the system re-runs the research step with refined queries until it produces a fully supported answer.

### Workflow

```
User query
   │
   ▼
Check relevance ──(irrelevant)──► Respond "out of scope" ──► End
   │ (relevant)
   ▼
Research ──► Verify ──(unsupported / contradicted)──► Re-research
   │ (verified)
   ▼
Return answer + verification report
```

The workflow is implemented as a stateful graph, where each stage (relevance check, research, verification) is a node, and conditional edges route execution based on the outcome of each step.

## Architecture

| Component | Role |
|---|---|
| **Document Processor** | Parses uploaded files (PDF, DOCX, TXT, MD) into structured Markdown, chunks them by header, and caches results to avoid reprocessing |
| **Retriever Builder** | Builds a hybrid retriever combining BM25 lexical search and vector similarity search over a persistent vector store |
| **Relevance Checker** | Classifies whether a question can be answered from the retrieved content (`CAN_ANSWER`, `PARTIAL`, `NO_MATCH`) |
| **Research Agent** | Generates a draft answer strictly grounded in retrieved context |
| **Verification Agent** | Checks the draft answer for factual support, contradictions, and relevance, producing a structured verification report |
| **Agent Workflow** | Orchestrates the above agents as a graph-based, stateful multi-agent system with loops and conditional transitions |
| **Web UI** | A simple, interactive front end for uploading documents, submitting questions, and viewing answers alongside their verification reports |

## Tech Stack

- **Document parsing & chunking**: [Docling](https://github.com/DS4SD/docling) — high-precision parsing of complex layouts, tables, and scanned documents (with OCR)
- **Multi-agent orchestration**: [LangGraph](https://github.com/langchain-ai/langgraph) — graph-based state machines for coordinating agents
- **Vector store**: [ChromaDB](https://www.trychroma.com/) — fast, persistent vector similarity search
- **RAG framework**: [LangChain](https://www.langchain.com/) — retrieval and chunking utilities
- **Web interface**: [Gradio](https://www.gradio.app/) — simple, interactive UI for document upload and Q&A
- **LLM & embeddings**: pluggable — bring your own LLM provider and embedding model of choice

## Getting Started

### Prerequisites

- Python 3.11+
- An API key/credentials for your LLM provider of choice (used for the research, verification, and relevance-checking agents, plus embeddings)

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/docchat.git
cd docchat

# Create and activate a virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Set your LLM provider credentials as environment variables (see `config/` for the expected settings), and adjust retrieval parameters — such as hybrid retriever weights and top-k values — as needed for your use case.

### Running the App

```bash
python app.py
```

Once running, open the app in your browser (default: `http://127.0.0.1:5000`). Upload a document (or select one of the built-in examples), enter your question, and hit submit.

**Note:** DocChat only accepts documents in these formats: `.pdf`, `.docx`, `.txt`, `.md`.

## Project Structure

```
docchat/
├── agents/              # Relevance checker, research agent, verification agent
├── config/              # Settings and constants
├── document_cache/      # Cached processed document chunks
├── document_processor/  # Docling-based document parsing and chunking
├── retriever/           # Hybrid (BM25 + vector) retriever builder
├── utils/               # Shared helper utilities
├── app.py               # Gradio application entry point
└── requirements.txt      # Python dependencies
```

## Limitations & Ideas for Extension

- **Embeddings**: try different embedding models to compare retrieval quality
- **Retrieval tuning**: adjust hybrid retriever weights, ranking logic, or add post-processing for better answer synthesis
- **Guardrails**: add moderation or safety layers for responsible AI usage
- **Workflow tuning**: refine verification heuristics or add richer self-correction feedback loops
- **Deployment**: containerize and deploy to a cloud platform of your choice
- **UI**: extend the Gradio interface with chat history, multi-turn context, or document annotations

## License

This project is licensed under the Apache 2.0 License.

## Acknowledgments

Built as a hands-on exploration of multi-agent RAG systems, combining document-aware parsing, hybrid retrieval, and verification-driven generation.
