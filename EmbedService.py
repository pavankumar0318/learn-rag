import tempfile

from langchain_community.document_loaders import PyPDFLoader
from pdfminer.high_level import extract_text
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from RAGService import RAGService
import os

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


class PDFEmbedService:
    def __init__(self, upload_dir="./uploaded_pdfs"):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)
        self.rag_service = RAGService()

    def save_and_embed(self, file_name, file_bytes):
        # Write bytes to a temp file so PyPDFLoader can read it
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        # Load with PyPDFLoader — this auto-attaches page numbers in metadata
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()  # each page is a Document with metadata

        # Attach the real filename to each page's metadata
        for page in pages:
            page.metadata["source"] = file_name  # ✅ override tmp path with real name

        # Split into chunks, metadata is preserved automatically
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(pages)  # ✅ use split_documents, not split_text

        os.unlink(tmp_path)  # clean up temp file
        # return chunks
        self.rag_service.embed_and_store(chunks)
        # return temp_path
