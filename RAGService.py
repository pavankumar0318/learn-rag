import os
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA
from Models import Models

_models = Models()
PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_index")


class RAGService:
    def __init__(self):
        tiktoken_cache = os.getenv("TIKTOKEN_CACHE_DIR", "./tiktoken_cache")
        os.makedirs(tiktoken_cache, exist_ok=True)
        os.environ["TIKTOKEN_CACHE_DIR"] = tiktoken_cache

        self.llm             = _models.chatModel()
        self.embedding_model = _models.embeddingModel()

    # ── Embed & store ─────────────────────────────────────────────────────────
    def embed_and_store(self, chunks, persist_directory: str = PERSIST_DIR):
        """
        Append chunks to an existing Chroma collection.
        Uses add_documents so re-running doesn't duplicate the entire index.
        """
        vectordb = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embedding_model,
        )
        vectordb.add_documents(chunks)
        return vectordb

    # ── Retriever ─────────────────────────────────────────────────────────────
    def get_retriever(self, persist_directory: str = PERSIST_DIR):
        vectordb = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embedding_model,
        )
        return vectordb.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5},
        )

    # ── RAG query ─────────────────────────────────────────────────────────────
    def invoke_rag(self, query: str, persist_directory: str = PERSIST_DIR) -> dict:
        """
        Invoke RAG to answer a query based on all embedded PDF content.
        Returns answer + source metadata for citation display.
        """
        retriever = self.get_retriever(persist_directory)
        rag_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=retriever,
            return_source_documents=True,
        )
        result = rag_chain.invoke(query)

        sources = [
            {
                "page":    doc.metadata.get("page", "N/A"),
                "source":  doc.metadata.get("source", "N/A"),
                "snippet": doc.page_content[:200],
            }
            for doc in result.get("source_documents", [])
        ]

        return {
            "answer":  result["result"],
            "sources": sources,
        }