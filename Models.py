
import os
import ssl

import httpx
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

class Models:

    def __init__(self):
        base_url = os.getenv("BASE_URL")
        llm_model = os.getenv("LLM_MODEL")
        embedding_model = os.getenv("EMBEDDING_MODEL")
        api_key = os.getenv("API_KEY")
        
        if not all([base_url, llm_model, embedding_model, api_key]):
            raise ValueError("Missing required environment variables: BASE_URL, LLM_MODEL, EMBEDDING_MODEL, or API_KEY")
        
        client = httpx.Client(verify=False)
        ssl._create_default_https_context = ssl._create_unverified_context
        # os.environ["TIKTOKEN_CACHE_DIR"] = r"C:\\Users\\GenAIBLRANCUSR64\\Desktop\\tittoken_cache"
        # self.llm = ChatOpenAI(
        #     base_url=base_url,
        #     model=llm_model, # type: ignore
        #     api_key=api_key, # type: ignore
        #     http_client=client
        # )
        # self.embedding_model = OpenAIEmbeddings(
            # base_url=base_url,
            # model=embedding_model, # type: ignore
            # api_key=api_key, # type: ignore
            # http_client=client
        # )

        self.llm = ChatOllama(
            model="gemma4:latest", # type: ignore
        )

        self.embedding_model = OllamaEmbeddings(
            model="nomic-embed-text-v2-moe:latest", # type: ignore
        )


    def chatModel(self):
        return self.llm

    def emmbedModel(self):
        return self.embedding_model