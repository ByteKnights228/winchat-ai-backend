from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
import logging
from langchain.schema import Document


from dotenv import load_dotenv
import os

logger = logging.getLogger("__main__")


class SimpleLLMSummarizer:
    PROMPT_TEMPLATE = """
    Summazrise the following text and give back only the summary. :

    {query_text}

    Note: THE OUTPUT SHOULD CONTAIN ONLY THE ACTUAL SUMMARY. DONT INCLUDE THE ORIGINAL TEXT. DO NOT INCLUDE ANYTHING ELSE IN THE OUTPUT.

    """

    def __init__(self, model: str, base_url: str, api_secret: str) -> None:
        self.model = model
        self.base_url = base_url
        self.api_secret = api_secret

    def summarize(self, query_text: str) -> str:
        prompt_template = ChatPromptTemplate.from_template(
            self.PROMPT_TEMPLATE)
        prompt = prompt_template.format(query_text=query_text)

        model = Ollama(
            model=self.model,
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_secret}"
            })
        response_text = model.invoke(prompt)

        return response_text

    def summarize_list(self, docs: list[Document]) -> list:
        logger.info(f"Summarizing list of {len(docs)} documents")
        i = 0
        for doc in docs:
            text = doc.page_content
            res = self.summarize(text)
            doc.page_content = res
            if i % 10 == 0:
                logger.info(f"Summarzed  {i} documents")
            i += 1
        return docs
