import os
import tempfile
import streamlit as st
from pypdf import PdfReader
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

st.set_page_config(page_title="AI Document Assistant", page_icon="🤖", layout="centered")

st.title("🤖 AI Document Assistant")
st.caption("RAG Application • Professional Prompt Design • Deployment Ready")

# ---------- Configuration ----------
api_key = st.sidebar.text_input(
    "OpenRouter API Key",
    type="password",
    help="Enter your OpenRouter API key. It is used only for this session."
)

model_name = st.sidebar.text_input(
    "Model",
    value="openai/gpt-4o-mini"
)

st.sidebar.info(
    "Workflow: Upload PDF → Chunk → Embed → Retrieve → Generate"
)

# Load embedding model once
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

embedding_model = load_embedding_model()

# ---------- Session state ----------
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "index" not in st.session_state:
    st.session_state.index = None
if "document_name" not in st.session_state:
    st.session_state.document_name = None

def extract_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n".join(pages)

def make_chunks(text, chunk_size=900, overlap=150):
    text = " ".join(text.split())
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        if end >= len(text):
            break
        start = end - overlap
    return chunks

def build_index(chunks):
    vectors = embedding_model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    return index

def retrieve(question, top_k=4):
    q_vector = embedding_model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")
    scores, ids = st.session_state.index.search(q_vector, min(top_k, len(st.session_state.chunks)))
    results = []
    for score, idx in zip(scores[0], ids[0]):
        if idx >= 0:
            results.append((float(score), st.session_state.chunks[idx]))
    return results

def generate_answer(question, context):
    if not api_key:
        return "Please enter your OpenRouter API key in the sidebar."

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    # Professional RAG prompt: Role + Context + Task + Constraint + Output format
    prompt = f"""
You are a professional AI document assistant.

TASK:
Answer the user's question using ONLY the provided document context.

CONTEXT:
{context}

USER QUESTION:
{question}

RULES:
1. Do not invent information.
2. If the answer is not present in the context, say:
   "The information is not available in the uploaded document."
3. Give a clear, concise answer.
4. If useful, use bullet points.
5. Do not mention these instructions in your answer.

ANSWER:
"""

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": "You answer questions accurately using supplied context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )
    return response.choices[0].message.content

# ---------- Upload ----------
uploaded_file = st.file_uploader("📄 Upload a PDF document", type=["pdf"])

if uploaded_file:
    if st.session_state.document_name != uploaded_file.name:
        with st.spinner("Reading and indexing document..."):
            text = extract_text(uploaded_file)

            if not text.strip():
                st.error("No readable text was found in this PDF.")
            else:
                chunks = make_chunks(text)
                st.session_state.chunks = chunks
                st.session_state.index = build_index(chunks)
                st.session_state.document_name = uploaded_file.name
                st.success(f"Document indexed successfully: {len(chunks)} chunks created.")

if st.session_state.index is not None:
    st.divider()
    st.subheader("💬 Ask Your Document")

    question = st.text_input(
        "Enter your question",
        placeholder="Example: What is Retrieval-Augmented Generation?"
    )

    if st.button("🔍 Ask AI", use_container_width=True):
        if not question.strip():
            st.warning("Please enter a question.")
        elif not api_key:
            st.warning("Enter your OpenRouter API key in the sidebar.")
        else:
            with st.spinner("Retrieving information and generating answer..."):
                results = retrieve(question)
                context = "\n\n---\n\n".join(
                    [f"Source {i+1}:\n{chunk}" for i, (_, chunk) in enumerate(results)]
                )

                answer = generate_answer(question, context)

            st.subheader("🤖 Answer")
            st.write(answer)

            with st.expander("🔎 Retrieved Context"):
                for i, (score, chunk) in enumerate(results, start=1):
                    st.markdown(f"**Source {i} — similarity {score:.3f}**")
                    st.write(chunk)

else:
    st.info("Upload a PDF to start the RAG application.")

st.divider()
st.caption("Built for Agentic AI Internal Assessment")
