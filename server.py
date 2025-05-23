from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime

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

app = Flask(__name__)
CORS(app)

# Store conversation histories (in-memory storage)
conversation_histories = {}

# Helper function to process queries
def process_query(query_text, session_id):
    embedding_function = OllamaEmbeddings(
        model=EMBEDDING_MODEL_NAME,
        base_url=OLLAMA_BASE_URL,
        headers={"Authorization": f"Bearer {OLLAMA_API_SECRET}"}
    )

    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    history = conversation_histories.get(session_id, [])
    formatted_history = "\n".join(
        [f"User: {entry['query']}\nBot: {entry['response']}" for entry in history]
    )

    articles = []
    sources = []
    results = db.similarity_search_with_relevance_scores(query_text, k=10)
    for res in results:
        source = res[0].metadata["source"]
        if res[1] < 0.5:
            continue
        if source not in sources:
            sources.append((source, res[1]))
            with open(source, "r", encoding="utf-8") as f:
                source_text = f.read()
                articles.append(source_text)

    context_text = "\n\n---\n\n".join(articles)

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, history=formatted_history, question=query_text)

    model = Ollama(
        model=CHAT_MODEL_NAME,
        base_url=OLLAMA_BASE_URL,
        headers={"Authorization": f"Bearer {OLLAMA_API_SECRET}"}
    )
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


# Initialize Flask app
app = Flask(__name__)
CORS(app)


@app.route("/api/health", methods=["GET"])
def health():

    """
    Health check endpoint.

    Returns:
        JSON response with status "ok".
    """

    return jsonify({"status": "ok"})

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Handle chat requests.

    Returns:
        JSON response with the bot's response.    
    """
    data = request.json
    query_text = data.get("query", "")
    session_id = data.get("session_id", str(uuid.uuid4()))

    if not query_text:
        return jsonify({"error": "Query text is required"}), 400

    try:
        # Process the query (Assume process_query is defined elsewhere)
        result = process_query(query_text, session_id)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def route_not_found(e):
    """
    Handle any unmatched routes to keep API sanity.

    Returns:
        JSON response with a 404 status code.
    """
    return jsonify({"error": "Route not found. Please check the API documentation for valid endpoints."}), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

