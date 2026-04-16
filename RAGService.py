from ast import Mod

from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA

from Models import Models


model = Models()


class RAGService:
    def __init__(self):
        # # Validate required environment variables
        # base_url = os.getenv("BASE_URL")
        # llm_model = os.getenv("LLM_MODEL")
        # embedding_model = os.getenv("EMBEDDING_MODEL")
        # api_key = os.getenv("API_KEY")

        # if not all([base_url, llm_model, embedding_model, api_key]):
        #     raise ValueError("Missing required environment variables: BASE_URL, LLM_MODEL, EMBEDDING_MODEL, or API_KEY")

        # client = httpx.Client(verify=False)
        # ssl._create_default_https_context = ssl._create_unverified_context
        # os.environ["TIKTOKEN_CACHE_DIR"] = r"C:\\Users\\GenAIBLRANCUSR64\\Desktop\\tittoken_cache"
        # self.llm = ChatOpenAI(
        #     base_url=base_url,
        #     model=llm_model, # type: ignore
        #     api_key=api_key, # type: ignore
        #     http_client=client
        # )
        # self.embedding_model = OpenAIEmbeddings(
        #     # base_url=base_url,
        #     # model=embedding_model, # type: ignore
        #     # api_key=api_key, # type: ignore
        #     # http_client=client
        # )
        self.llm = model.chatModel()
        self.embedding_model = model.emmbedModel()

    def embed_and_store(self, chunks, persist_directory="./chroma_index"):
        vectordb = Chroma.from_documents(
            chunks, self.embedding_model, persist_directory=persist_directory
        )
        # vectordb.persist()
        return vectordb

    def get_retriever(self, persist_directory="./chroma_index"):
        vectordb = Chroma(
            persist_directory=persist_directory, embedding_function=self.embedding_model
        )
        return vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    # @tool
    def invoke_rag(self, query, persist_directory="./chroma_index"):
        """Invoke RAG to answer a query based on embedded PDF content."""
        retriever = self.get_retriever(persist_directory)
        rag_chain = RetrievalQA.from_chain_type(
            llm=self.llm, retriever=retriever, return_source_documents=True
        )
        result = rag_chain.invoke(query)

        sources = [
            {
                "page": doc.metadata.get("page", "N/A"),
                "source": doc.metadata.get("source", "N/A"),
                "snippet": doc.page_content[:200]  # first 200 chars as preview
            }
            for doc in result.get("source_documents", [])
        ]

        return {
            "answer": result["result"],
            "sources": sources
        }
