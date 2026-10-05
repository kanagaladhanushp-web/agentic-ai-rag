import os
import tempfile
import streamlit as st
from pypdf import PdfReader
from openai import OpenAI

st.set_page_config(page_title="AI Document Assistant", page_icon="🤖", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --ink: #172b32;
        --muted: #64767b;
        --line: #dce6e4;
        --paper: #f5f8f6;
        --teal: #087e78;
        --teal-dark: #075e5a;
        --mint: #e7f4f0;
        --coral: #d9825b;
    }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: var(--paper); color: var(--ink); }
    [data-testid="stHeader"] { background: rgba(245, 248, 246, .92); }
    [data-testid="stMainBlockContainer"] { max-width: 1180px; padding-top: 2rem; padding-bottom: 1rem; }
    [data-testid="stSidebar"] { background: #edf4f1; border-right: 1px solid var(--line); }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: var(--muted); }
    h1, h2, h3 { font-family: 'Manrope', sans-serif; color: var(--ink); letter-spacing: 0; }
    .hero { padding: .75rem 0 1.65rem; border-bottom: 1px solid var(--line); margin-bottom: 1.6rem; }
    .hero-kicker { color: var(--teal); font-size: .76rem; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; }
    .hero-title { margin: .35rem 0 .2rem; font: 800 2.05rem/1.2 'Manrope', sans-serif; color: var(--ink); }
    .hero-subtitle { color: var(--muted); font-size: 1rem; margin: 0; }
    .hero-meta { display: inline-flex; align-items: center; gap: .55rem; margin-top: .9rem; padding: .38rem .7rem; background: #eaf3f0; border: 1px solid #d8e7e2; border-radius: 999px; color: #58716d; font-size: .76rem; }
    .hero-meta strong { color: var(--teal-dark); font-size: .7rem; letter-spacing: .06em; }
    .hero-meta-dot { width: .38rem; height: .38rem; border-radius: 50%; background: var(--coral); }
    .section-title { margin: .2rem 0 .25rem; font: 700 1.32rem 'Manrope', sans-serif; color: var(--ink); }
    .section-note { color: var(--muted); font-size: .92rem; margin: 0 0 1rem; }
    [data-testid="stFileUploader"] section { background: #fff; border: 1.5px dashed #9bbab3; border-radius: 12px; padding: 1.35rem; transition: border-color .18s ease, background .18s ease; }
    [data-testid="stFileUploader"] section:hover { border-color: var(--teal); background: #fafffd; }
    [data-testid="stFileUploader"] button { border-radius: 7px; border-color: #aac5bf; color: var(--teal-dark); }
    [data-testid="stMetric"] { background: #fff; border: 1px solid var(--line); border-radius: 9px; padding: .95rem 1rem; transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease; }
    [data-testid="stMetric"]:hover { transform: translateY(-2px); border-color: #bdd6d0; box-shadow: 0 8px 22px #274b4210; }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    [data-testid="stMetricValue"] { color: var(--ink); font-family: 'Manrope', sans-serif; }
    div.stButton > button { border-radius: 7px; font-weight: 700; min-height: 2.8rem; transition: transform .15s ease, box-shadow .15s ease; }
    div.stButton > button[kind="primary"] { background: var(--teal); border-color: var(--teal); color: #fff; }
    div.stButton > button[kind="primary"]:hover { background: var(--teal-dark); border-color: var(--teal-dark); box-shadow: 0 5px 14px #087e7828; transform: translateY(-1px); }
    [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea { border-radius: 8px; background: #fff; border-color: #cbd9d6; }
    [data-testid="stChatMessage"] { background: #fff; border: 1px solid var(--line); border-radius: 10px; padding: 1rem 1.2rem; animation: rise-in .45s ease-out both; }
    [data-testid="stExpander"] { background: #fff; border: 1px solid var(--line); border-radius: 9px; transition: border-color .18s ease, box-shadow .18s ease; }
    [data-testid="stExpander"]:hover { border-color: #bdd6d0; box-shadow: 0 5px 16px #274b420c; }
    [data-testid="stAlert"] { border-radius: 8px; }
    .question-examples { display: flex; flex-wrap: wrap; gap: .45rem; margin: .15rem 0 1.1rem; }
    .question-chip { border: 1px solid #d4e3df; background: #edf5f2; color: #42605c; border-radius: 6px; padding: .33rem .6rem; font-size: .79rem; }
    .sidebar-heading { font: 700 1.1rem 'Manrope', sans-serif; color: var(--ink); margin: .2rem 0 .9rem; }
    .workflow-step { display: flex; gap: .65rem; align-items: flex-start; margin: .75rem 0; color: #455c5b; font-size: .9rem; }
    .step-number { flex: 0 0 1.5rem; height: 1.5rem; border-radius: 50%; display: grid; place-items: center; background: var(--mint); color: var(--teal-dark); font-weight: 700; font-size: .77rem; }
    .footer { border-top: 1px solid var(--line); padding: 1rem 0 .4rem; margin-top: 2rem; color: #71827f; text-align: center; font-size: .8rem; }
    @keyframes rise-in { from { opacity: 0; transform: translateY(9px); } to { opacity: 1; transform: translateY(0); } }
    .hero { animation: rise-in .55s ease-out both; }
    .hero-meta { animation: rise-in .55s .12s ease-out both; }
    .section-title { animation: rise-in .4s ease-out both; }
    div.stButton > button:focus-visible { outline: 3px solid #79b9ac; outline-offset: 2px; }
    @media (max-width: 700px) {
        [data-testid="stMainBlockContainer"] { padding: 1.1rem 1rem .5rem; }
        .hero-title { font-size: 1.65rem; }
        .hergit so { padding-top: .35rem; }
    }
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: .01ms !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <header class="hero">
        <div class="hero-kicker">Document intelligence</div>
        <div class="hero-title">🤖 AI Document Assistant</div>
        <p class="hero-subtitle">Intelligent Document Question Answering using RAG</p>
        <div class="hero-meta"><span class="hero-meta-dot"></span><strong>RAG WORKSPACE</strong><span>PDF · Retrieval · AI answers</span></div>
    </header>
    """,
    unsafe_allow_html=True,
)

# ---------- Configuration ----------
st.sidebar.markdown('<div class="sidebar-heading">Workspace settings</div>', unsafe_allow_html=True)
api_key = st.sidebar.text_input(
    "OpenRouter API Key",
    type="password",
    help="Enter your OpenRouter API key. It is used only for this session."
)

model_name = st.sidebar.text_input(
    "Model",
    value="openai/gpt-4o-mini"
)

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-heading">How it works</div>', unsafe_allow_html=True)
st.sidebar.markdown(
    """
    <div class="workflow-step"><span class="step-number">1</span><span>Upload a PDF document</span></div>
    <div class="workflow-step"><span class="step-number">2</span><span>Retrieve relevant information</span></div>
    <div class="workflow-step"><span class="step-number">3</span><span>Generate a grounded AI answer</span></div>
    """,
    unsafe_allow_html=True,
)

# Load embedding model once
@st.cache_resource
def load_embedding_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer("all-MiniLM-L6-v2")

# ---------- Session state ----------
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "index" not in st.session_state:
    st.session_state.index = None
if "document_name" not in st.session_state:
    st.session_state.document_name = None
if "page_count" not in st.session_state:
    st.session_state.page_count = 0

def extract_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n".join(pages), len(reader.pages)

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
    import faiss
    import numpy as np

    embedding_model = load_embedding_model()
    vectors = embedding_model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    return index

def retrieve(question, top_k=4):
    import numpy as np

    embedding_model = load_embedding_model()
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
st.markdown('<div class="section-title">Your document</div>', unsafe_allow_html=True)
st.markdown('<p class="section-note">Add a PDF to build a searchable knowledge base.</p>', unsafe_allow_html=True)
st.markdown("### 📄 Upload your document")
st.caption("Supported format: PDF")
uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"], label_visibility="collapsed")

if uploaded_file:
    if st.session_state.document_name != uploaded_file.name:
        with st.spinner("Reading and indexing document..."):
            text, page_count = extract_text(uploaded_file)

            if not text.strip():
                st.error("No readable text was found in this PDF.")
            else:
                chunks = make_chunks(text)
                st.session_state.chunks = chunks
                st.session_state.index = build_index(chunks)
                st.session_state.document_name = uploaded_file.name
                st.session_state.page_count = page_count
                st.success("Document indexed successfully and ready for questions.")

if st.session_state.index is not None:
    st.markdown("#### Indexed document")
    st.caption(f"📄 {st.session_state.document_name}")
    stat_columns = st.columns(3)
    stat_columns[0].metric("Pages", st.session_state.page_count)
    stat_columns[1].metric("Text chunks", len(st.session_state.chunks))
    stat_columns[2].metric("Status", "Ready")

    st.divider()
    st.markdown('<div class="section-title">Ask your document</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-note">Ask a question and get an answer grounded in your uploaded PDF.</p>', unsafe_allow_html=True)

    question = st.text_area(
        "Your question",
        placeholder="Ask something about the document...",
        height=105,
        label_visibility="collapsed",
    )
    st.markdown(
        """
        <div class="question-examples">
            <span class="question-chip">Summarize the main ideas</span>
            <span class="question-chip">What are the key findings?</span>
            <span class="question-chip">Explain the central topic</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Ask AI  →", type="primary", use_container_width=True):
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

            st.markdown("#### 🤖 AI Assistant")
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(answer or "The assistant returned an empty response.")

            with st.expander("Retrieved Context  ·  Sources used to ground this answer"):
                for i, (score, chunk) in enumerate(results, start=1):
                    st.markdown(f"**Source {i}** · Similarity {score:.3f}")
                    st.markdown(chunk)
                    if i < len(results):
                        st.divider()

else:
    st.info("Upload a PDF to start asking questions about your document.")

st.markdown(
    '<footer class="footer">AI Document Assistant • RAG-based Intelligent Question Answering</footer>',
    unsafe_allow_html=True,
)
