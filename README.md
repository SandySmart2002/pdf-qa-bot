Below is the **README** for your project, outlining the core elements of the QA bot system, setup, and usage.

---

# **QA Bot with FastAPI and Streamlit**

## **Overview**

This project is a **Question Answering (QA) bot** that allows users to upload PDF documents and ask questions based on the document's content. The system uses **Cohere** for natural language processing and **Pinecone** for vector storage and retrieval, providing accurate and contextually relevant answers.

### **Features**:
- Upload PDF documents and extract content.
- Store document embeddings in Pinecone for efficient retrieval.
- Answer user queries based on the uploaded document.
- Containerized for easy deployment with **Docker**.

---

## **Tech Stack**

- **FastAPI**: Backend for handling PDF uploads, document embedding, and querying.
- **Streamlit**: Frontend for user interaction and input.
- **Cohere**: Embedding and text generation for questions and answers.
- **Pinecone**: Vector database to store and retrieve document embeddings.
- **Docker**: For containerization of frontend and backend.
  
---

## **Getting Started**

### **Prerequisites**

Before setting up the project, ensure you have the following:
- **Python 3.9+**
- **Docker** and **Docker Compose**
- API keys from:
  - **Pinecone** ([pinecone.io](https://www.pinecone.io/))
  - **Cohere** ([cohere.ai](https://cohere.ai/))

### **Installation**

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/qa-bot.git
   cd qa-bot
   ```

2. Add your API keys:
   - In `backend/main.py`, replace:
     ```python
     pinecone.init(api_key="YOUR_PINECONE_API_KEY")
     cohere_client = cohere.Client("YOUR_COHERE_API_KEY")
     ```
   - with your actual API keys from Pinecone and Cohere.

---

## **Running the Project**

### **Option 1: Docker Compose**

The easiest way to get the project running is by using Docker Compose to spin up both the FastAPI backend and Streamlit frontend.

1. Build and run the containers:
   ```bash
   docker-compose up --build
   ```

2. Access the frontend:
   - **Streamlit**: `http://localhost:8501`
   - **FastAPI**: `http://localhost:8000`

### **Option 2: Running Locally**

If you prefer to run the services locally without Docker, follow these steps:

#### **Backend (FastAPI)**

1. Navigate to the backend directory and install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

#### **Frontend (Streamlit)**

1. Navigate to the frontend directory and install dependencies:
   ```bash
   cd frontend
   pip install -r requirements.txt
   ```

2. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

---

## **Usage**

### **1. Upload a PDF**
- Use the Streamlit interface to upload a PDF document.
- The document is processed, split into chunks, and embeddings are stored in Pinecone.

### **2. Ask a Question**
- After the PDF is uploaded, enter a question in the Streamlit input field.
- The system will retrieve the most relevant document chunks and generate an answer using Cohere.

---

## **API Endpoints**

### **Backend Endpoints**

1. **POST `/upload/`**: Upload a PDF file to process and store document embeddings.
2. **POST `/query/`**: Send a question to retrieve and generate an answer from stored document embeddings.
3. **GET `/health/`**: Check the health of the API.

---

## **Project Structure**

qa-bot/
├── backend/
│   ├── main.py  # FastAPI backend code
│   ├── requirements.txt  # Backend dependencies
├── frontend/
│   ├── app.py  # Streamlit frontend code
│   ├── requirements.txt  # Frontend dependencies
├── Dockerfile  # Docker configuration for both frontend and backend
├── docker-compose.yml  # Docker Compose setup
