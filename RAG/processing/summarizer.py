from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
import logging
from langchain.schema import Document


from dotenv import load_dotenv
import os

logger = logging.getLogger("__main__")


class SimpleLLMSummarizer:
    PROMPT_TEMPLATE = """
    Summazrise the following text and give back only the summary. :
    Note: THE OUTPUT SHOULD CONTAIN ONLY THE ACTUAL SUMMARY. DONT INCLUDE THE ORIGINAL TEXT. DO NOT INCLUDE ANYTHING ELSE IN THE OUTPUT.

    {query_text}


    """

    def __init__(self, model: str, base_url: str, api_secret: str) -> None:
        self.model = model
        self.base_url = base_url
        self.api_secret = api_secret

        logger.info(f"SimpleLLMSummarizer initialized with model: {model}")
        logger.info(f"SimpleLLMSummarizer initialized with base_url: {base_url}")
        logger.info(f"SimpleLLMSummarizer initialized with api_secret: {api_secret}")

    def summarize(self, query_text: str) -> str:
        prompt_template = ChatPromptTemplate.from_template(
            self.PROMPT_TEMPLATE)
        prompt = prompt_template.format(query_text=query_text)

        model = OllamaLLM(
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
    def save_list(self, summaries:list[Document], save_dir:str="./summaries" ) -> list[str]:
        """
        Save the summaries to a file

        """
        if not os.path.exists(save_dir):
                os.makedirs(save_dir)

        logger.info(f"Saving summaries to {os.path.abspath(save_dir)}")

        file_names = []

        for summary in summaries:
            
            source_file_name = summary.metadata["source"].split("/")[-1]

            file_name = f"{save_dir}/{source_file_name}"

            with open(file_name, "w") as f: 
                f.write(summary.page_content)

            file_names.append(file_name)

        return file_names      

        

      
       

        

        





if __name__ == "__main__":
    # get all keys from .env file
    EMBEDDING_MODEL_NAME = "qwen2"
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
    OLLAMA_API_SECRET = os.getenv("OLLAMA_SECRET")

    summarizer = SimpleLLMSummarizer(
        model=EMBEDDING_MODEL_NAME,
        base_url=OLLAMA_BASE_URL,
        api_secret=OLLAMA_API_SECRET,
    )

    query_text = """
    ## Question
    A required Canadian Tax return was not filed for my OSAP application, what should I do?
    ## Answer

    For OSAP purposes, individuals with a Social Insurance Number (SIN) are expected to file a tax return to Canada Revenue Agency (CRA) even if they had zero income in order that the Ministry can ensure that the student is eligible for the funding provided to them. If an individual has not filed their tax return, they should do so as soon as possible.
    An individual cannot file a tax return if they do not possess a SIN, recently moved to Canada, are not legally entitled to work, or earn income on a First Nations Reserve. In these cases, a letter, along with proof of the situation, must be provided to the Financial Aid Office for review.
    For those whose spouses or parents are not living in Canada, the equivalent of Canada's CRA Notice of Assessment/income tax documentation is required. Students will be asked to submit Proof of Parental/Spousal income by completing a form entitled “Parent (or Spouse) Income Verification: Canadian Non-Taxable and/or Foreign Income” and provide all documentation requested.
    Visit the Student Awards and Financial Aid website for more information about OSAP and the appeal section here: http://www.uwindsor.ca/studentawards/appeal-forms to find information about other special situations.
    """
    summary = summarizer.summarize(query_text)
    print(summary)
    print("Done")