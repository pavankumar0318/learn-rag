import os
import tempfile

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from RAGService import RAGService

CHUNK_SIZE    = 500
CHUNK_OVERLAP = 50


class PDFEmbedService:
    def __init__(self, upload_dir: str = "./uploaded_pdfs"):
        self.upload_dir  = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)
        self.rag_service = RAGService()

    def save_and_embed(self, file_name: str, file_bytes: bytes) -> None:
        """
        Write PDF bytes to a temp file, load with PyPDFLoader (preserves page
        metadata), chunk with RecursiveCharacterTextSplitter, then append to
        the shared Chroma index.
        """
        # Write to temp file — PyPDFLoader requires a real path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.namex

        try:
            loader = PyPDFLoader(tmp_path)
            pages  = loader.load()

            # Override tmp path with the real filename in metadata
            for page in pages:
                page.metadata["source"] = file_name

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP,
            )
            chunks = splitter.split_documents(pages)
        finally:
            os.unlink(tmp_path)  # always clean up

        self.rag_service.embed_and_store(chunks)