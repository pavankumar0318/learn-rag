import os
import ssl

import httpx
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()


class Models:

    def __init__(self):
        base_url       = os.getenv("BASE_URL")
        llm_model      = os.getenv("LLM_MODEL")
        embedding_model = os.getenv("EMBEDDING_MODEL")
        api_key        = os.getenv("API_KEY")

        if not all([base_url, llm_model, embedding_model, api_key]):
            raise ValueError(
                "Missing required environment variables: BASE_URL, LLM_MODEL, EMBEDDING_MODEL, API_KEY"
            )

        # Disable SSL verification for corporate proxy environments
        client = httpx.Client(verify=False)
        ssl._create_default_https_context = ssl._create_unverified_context

        # Allow override via env; avoids hardcoded Windows path
        tiktoken_cache = os.getenv("TIKTOKEN_CACHE_DIR", "./tiktoken_cache")
        os.makedirs(tiktoken_cache, exist_ok=True)
        os.environ["TIKTOKEN_CACHE_DIR"] = tiktoken_cache

        
        self._llm = ChatOpenAI(
            base_url=base_url,
            model=llm_model,
            api_key=api_key,
            http_client=client,
        )
        self._embedding_model = OpenAIEmbeddings(
            base_url=base_url,
            model=embedding_model,
            api_key=api_key,
            http_client=client,
        )

    def chatModel(self):
        return self._llm

    def embeddingModel(self):
        return self._embedding_model