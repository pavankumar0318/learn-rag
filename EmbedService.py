from pdfminer.high_level import extract_text
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from RAGService import RAGService
import os

class PDFEmbedService:
    def __init__(self, upload_dir="./uploaded_pdfs"):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)
        self.rag_service = RAGService()

    def save_and_embed(self, file_name, file_bytes):
        temp_path = os.path.join(self.upload_dir, file_name)
        with open(temp_path, "wb") as f:
            f.write(file_bytes)
        raw_text = extract_text(temp_path)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(raw_text)
        self.rag_service.embed_and_store(chunks)
        return temp_path
