# 🤖 AI Document Assistant — RAG Application

A simple Retrieval-Augmented Generation (RAG) application for the Agentic AI practical assessment.

## Covers all 3 exercises

### Exercise 1 — RAG Application with UI
- PDF document ingestion
- Text extraction
- Text chunking
- Embeddings
- FAISS vector search
- Relevant context retrieval
- LLM answer generation
- Streamlit user interface

### Exercise 2 — Professional Prompt Design
The application uses a professional RAG prompt containing:
- Role
- Task
- Context
- User question
- Rules/constraints
- Output instructions

### Exercise 3 — Deployment
The project is GitHub-ready and can be deployed using Streamlit Community Cloud.

## 1. Install

Open the VS Code terminal:

```bash
python -m venv venv
```

Windows PowerShell:

```bash
venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use:

```bash
venv\Scripts\activate.bat
```

Install packages:

```bash
pip install -r requirements.txt
```

## 2. Run

```bash
streamlit run app.py
```

The browser will open the Streamlit application.

## 3. OpenRouter API key

Create an OpenRouter API key and enter it in the application sidebar.

Do NOT put your API key directly into `app.py`.

## 4. Test

Upload a text-based PDF.

Example questions:
- What is RAG?
- What are the main concepts in this document?
- Explain the topic in simple words.
- What are the important points?

## 5. GitHub

```bash
git init
git add .
git commit -m "Agentic AI RAG application"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

## 6. Deployment

Deploy the GitHub repository on Streamlit Community Cloud.

Main file:
```text
app.py
```

Python dependencies:
```text
requirements.txt
```

After deployment, open the generated `.streamlit.app` URL and demonstrate:
PDF upload → question → retrieval → AI answer.

## Architecture

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Sentence Transformer Embeddings
 ↓
FAISS Vector Database
 ↓
Question Embedding
 ↓
Top Relevant Chunks
 ↓
Professional RAG Prompt
 ↓
OpenRouter LLM
 ↓
Answer in Streamlit UI
```
