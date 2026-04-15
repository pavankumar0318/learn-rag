from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA
import httpx
import ssl
import os

class RAGService:
    def __init__(self):
        client = httpx.Client(verify=False)
        ssl._create_default_https_context = ssl._create_unverified_context
        os.environ["TIKTOKEN_CACHE_DIR"] = r"C:\\Users\\GenAIBLRANCUSR64\\Desktop\\tittoken_cache"
        self.llm = ChatOpenAI(
            base_url="https://genailab.tcs.in",
            model="azure_ai/genailab-maas-DeepSeek-V3-0324",
            api_key="sk-f86P8es9uGdSMYl2aWt-Lw",
            http_client=client
        )
        self.embedding_model = OpenAIEmbeddings(
            base_url="https://genailab.tcs.in",
            model="azure/genailab-maas-text-embedding-3-large",
            api_key="sk-f86P8es9uGdSMYl2aWt-Lw",
            http_client=client
        )

    def embed_and_store(self, chunks, persist_directory="./chroma_index"):
        vectordb = Chroma.from_texts(chunks, self.embedding_model, persist_directory=persist_directory)
        vectordb.persist()
        return vectordb

    def get_retriever(self, persist_directory="./chroma_index"):
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=self.embedding_model)
        return vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    def invoke_rag(self, query, persist_directory="./chroma_index"):
        retriever = self.get_retriever(persist_directory)
        rag_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=retriever,
            return_source_documents=True
        )
        return rag_chain.invoke(query)
