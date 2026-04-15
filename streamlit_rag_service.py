import streamlit as st
from pdfminer.high_level import extract_text
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
import tempfile
from RAGService import RAGService

rag_service = RAGService()

st.set_page_config(page_title="RAG PDF Summarizer (Service Refactor)")
st.title("     RAG-powered PDF Summarizer (Service Refactor)")
upload_file = st.file_uploader("Upload a PDF", type="pdf")

if upload_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(upload_file.read())
        temp_file_path = temp_file.name
    raw_text = extract_text(temp_file_path)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(raw_text)
    with st.spinner("Indexing document..."):
        rag_service.embed_and_store(chunks)
    summary_prompt = "Please summarize this document based on the key topics:"
    with st.spinner("Running RAG summarization..."):
        result = rag_service.invoke_rag(summary_prompt)
    st.subheader("     Summary")
    st.write(result)
