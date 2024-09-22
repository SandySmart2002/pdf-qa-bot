from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cohere
import pinecone
from pypdf import PdfReader
from typing import List
import io

# Initialize FastAPI app
app = FastAPI()

# Allow cross-origin requests (needed for Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Pinecone and Cohere
pinecone.init(api_key="YOUR_PINECONE_API_KEY", environment="us-west1-gcp")
index = pinecone.Index("qa-bot-index")

cohere_client = cohere.Client("YOUR_COHERE_API_KEY")

# Utility to split PDF into text chunks
def split_pdf_into_chunks(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    # Split into smaller chunks for better embedding accuracy
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    return chunks

# Endpoint to upload a PDF and process it
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Read the uploaded PDF
    pdf_file = io.BytesIO(await file.read())
    document_chunks = split_pdf_into_chunks(pdf_file)

    # Embed and store in Pinecone
    embeddings = []
    for i, chunk in enumerate(document_chunks):
        embedding = cohere_client.embed(texts=[chunk]).embeddings[0]
        # Store embeddings in Pinecone with metadata (e.g., chunk text)
        index.upsert(vectors=[(f"doc_chunk_{i}", embedding, {"text": chunk})])
        embeddings.append(embedding)

    return {"message": "Document processed and embeddings stored successfully!"}

# Endpoint to handle user queries
@app.post("/query/")
async def query_document(question: str):
    if not question:
        raise HTTPException(status_code=400, detail="Question is required.")

    # Create the query embedding
    query_embedding = cohere_client.embed(texts=[question]).embeddings[0]

    # Query Pinecone for the most relevant document chunks
    query_results = index.query(vector=query_embedding, top_k=3, include_metadata=True)

    # Extract relevant document texts
    relevant_documents = [result["metadata"]["text"] for result in query_results["matches"]]

    # Generate the answer using Cohere based on the retrieved documents
    prompt = f"Answer the question based on the following documents:\n{''.join(relevant_documents)}\n\nQuestion: {question}"
    response = cohere_client.generate(
        model="command-xlarge-nightly", prompt=prompt, max_tokens=200
    )

    # Return the answer
    answer = response.generations[0].text.strip()
    return {"answer": answer}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "API is healthy"}
