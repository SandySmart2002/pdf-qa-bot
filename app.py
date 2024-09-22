import streamlit as st
import requests

# FastAPI backend URL
BACKEND_URL = "http://localhost:8000"

# Streamlit UI
st.title("QA Bot Interface")
uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file:
    # Upload the file to the backend
    with st.spinner("Processing document..."):
        response = requests.post(
            f"{BACKEND_URL}/upload/", 
            files={"file": uploaded_file.getvalue()}
        )
        if response.status_code == 200:
            st.success("Document processed and embeddings stored successfully!")
        else:
            st.error(f"Error: {response.json()['detail']}")

query = st.text_input("Ask a question:")
if st.button("Get Answer"):
    if query:
        # Query the backend for the answer
        with st.spinner("Fetching the answer..."):
            response = requests.post(
                f"{BACKEND_URL}/query/",
                json={"question": query}
            )
            if response.status_code == 200:
                st.write("Answer:", response.json()["answer"])
            else:
                st.error(f"Error: {response.json()['detail']}")
    else:
        st.warning("Please enter a question.")
