from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
EMBEDDING_MODEL_NAME = os.getenv("OLLAMA_EMBEDDING_MODEL")
OLLAMA_API_SECRET = os.getenv("OLLAMA_SECRET")
CHAT_MODEL_NAME = os.getenv("OLLAMA_CHAT_MODEL")

CHROMA_PATH = "data\store\chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

## History
{history}

## Question
{question}

## Answer


NOTE: Don't add anything into the response other than the answer to the question.
"""

PROMPT_TEMPLATE_2 =""" You are an AI assistant. Follow these instructions when answering user queries:

Use Provided Context Only: Answer questions strictly based on the context provided in the `context` field. Do not include external information or make assumptions.

Ignore History Unless Specified: Only use the information in the `history` field if explicitly relevant to the query.

Focus on the Question: Address only the content in the `question` field. Do not add any extraneous information or commentary.

Output Format: Provide your response in the following format:

Answer: Directly answer the question.

Note: Always ensure your response is concise, precise, and strictly within the provided context.


===

Context: {context}

History: {history}

Question: {question}


"""


# Store conversation histories (in-memory storage)
conversation_histories = {}

model = OllamaLLM(
            model=CHAT_MODEL_NAME,
            base_url=OLLAMA_BASE_URL,
        )

# Helper function to process queries
def process_query(query_text, session_id):
    
    history = conversation_histories.get(session_id, [])
    formatted_history = "\n".join(
        [f"User: {entry['query']}\nBot: {entry['response']}" for entry in history]
    )

    articles = ["""
    ## Question
    A required Canadian Tax return was not filed for my OSAP application, what should I do?
    ## Answer

    For OSAP purposes, individuals with a Social Insurance Number (SIN) are expected to file a tax return to Canada Revenue Agency (CRA) even if they had zero income in order that the Ministry can ensure that the student is eligible for the funding provided to them. If an individual has not filed their tax return, they should do so as soon as possible.
    An individual cannot file a tax return if they do not possess a SIN, recently moved to Canada, are not legally entitled to work, or earn income on a First Nations Reserve. In these cases, a letter, along with proof of the situation, must be provided to the Financial Aid Office for review.
    For those whose spouses or parents are not living in Canada, the equivalent of Canada's CRA Notice of Assessment/income tax documentation is required. Students will be asked to submit Proof of Parental/Spousal income by completing a form entitled “Parent (or Spouse) Income Verification: Canadian Non-Taxable and/or Foreign Income” and provide all documentation requested.
    Visit the Student Awards and Financial Aid website for more information about OSAP and the appeal section here: http://www.uwindsor.ca/studentawards/appeal-forms to find information about other special situations.
    """]
    sources = ["data/store/test/A_required_Canadian_Tax_return_was_not_filed_for_my_OSAP_application_what_should_I_do.txt"]
   
    context_text = "\n\n---\n\n".join(articles)

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_2)
    prompt = prompt_template.format(context=context_text, history=formatted_history, question=query_text)

    response_text = model.invoke(prompt)

    history_entry = {"query": query_text, "response": response_text}
    if session_id not in conversation_histories:
        conversation_histories[session_id] = []
    conversation_histories[session_id].append(history_entry)

    return {
        "response": response_text,
        "sources": [src[0] for src in sources],
        "session_id": session_id
    }





if __name__ == "__main__":
    while True:
        input_text = input("Type exit to quit:")
        if input_text == "exit":
            break
        query_text = "I have a SIN so do I need to file a tax return?"
        session_id = "1"
       
        response = process_query(query_text, session_id)
        print(response["response"])
        print("Sources:")
        for src in response["sources"]:
            print(src)
        print("\n")
        