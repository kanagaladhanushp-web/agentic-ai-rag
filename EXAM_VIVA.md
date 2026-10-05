# Agentic AI Practical — Viva Preparation

## Exercise 1

### What is RAG?
RAG stands for Retrieval-Augmented Generation. It retrieves relevant information from a knowledge source and gives that information to an LLM as context before generating an answer.

### Why use RAG?
It helps an AI answer questions using specific documents and reduces unsupported answers.

### What is chunking?
Chunking divides a large document into smaller pieces so relevant information can be retrieved efficiently.

### What are embeddings?
Embeddings convert text into numerical vectors that represent semantic meaning.

### What is FAISS?
FAISS is a library used for efficient similarity search over vectors.

### What happens when the user asks a question?
The question is converted into an embedding, similar document chunks are retrieved, and the retrieved context is given to the LLM to generate the final answer.

## Exercise 2

### What makes a prompt professional?
A good prompt clearly defines the role, context, task, constraints, and expected output format.

### What is context?
Context is information supplied to the model to help it produce a relevant answer.

### Why specify constraints?
Constraints reduce unwanted or incorrect output.

## Exercise 3

### Why deploy the application?
Deployment makes the application accessible through a web URL instead of only running on the local computer.

### What files are required?
At minimum:
- app.py
- requirements.txt

### Explain your project in 30 seconds

"My project is an AI Document Assistant based on Retrieval-Augmented Generation. The user uploads a PDF through a Streamlit UI. The application extracts the text, divides it into chunks, converts the chunks into embeddings, and stores them in a FAISS vector index. When the user asks a question, the system retrieves the most relevant chunks and sends them with a professional prompt to an LLM through OpenRouter. The generated answer is displayed in the UI. The project can be uploaded to GitHub and deployed as a web application."
