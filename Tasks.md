# Tasks.md

## Pending Tasks

### 1. RAG Arch
- **Test Embedding Models**
  - mxbai-embed-large _ done
  - MiniLM
  - Instructor-XL (quantized)
- **Test Chat Models**
  - LLaMA 2 (7B)
  - GPT-J-6B
  - Falcon-7B (quantized)
- **Test Summarization Models**
  - LLaMA 2 (7B)
  - GPT-J-6B
  - Falcon-7B (quantized)
- **Write Tests**
  - Check time and load

### 2. Prompt Engineering
- **Test Different Prompts**
  - Experiment with new techniques to find answers.
- **Add Guardrails**
  - Address out-of-context content and explore additional methods for implementing guardrails.

### 3. Backend
- **Switch to NodeJS**
  - **Endpoints**
    1. **POST** `/api/chat`
       - **Request:**
         ```json
         {
           "query": "Bus pass and how do I get one",
           "session_id": "2"
         }
         ```
       - **Response:**
         ```json
         {
           "response": "The University of Windsor offers various programs with co-op options across disciplines...",
           "sources": ["data/store/main/Which_programs_offer_coop.txt"]
         }
         ```
    2. **GET** `/api/health`
       - **Response:**
         ```json
         {
           "status": "ok"
         }
         ```
    3. **GET** `http://127.0.0.1:5000/api/history?session_id=1`
       - **Response:**
         ```json
         {
           "created_at": "Sat, 28 Dec 2024 01:22:02 GMT",
           "history": [
             {
               "query": "What is the capital of Canada 2?",
               "response": "There is no information provided in the context about a 'Canada 2'.",
               "timestamp": "Sat, 28 Dec 2024 01:22:02 GMT"
             },
             {
               "query": "What is the capital of Canada 1?",
               "response": "I don't have that information.",
               "timestamp": "Sat, 28 Dec 2024 01:22:46 GMT"
             }
           ],
           "session_id": "1",
           "updated_at": "Sat, 28 Dec 2024 01:22:46 GMT"
         }
         ```
    4. **DELETE** `http://127.0.0.1:5000/api/history?session_id=1`
       - **Response:**
         ```json
         {
           "message": "Conversation history cleared"
         }
         ```
- **Create Flask Wrappers**
  - Microservice for chatting with Ollama model.

### 4. Frontend
- **Shift TQ**
  - Upgrade from v4 to v5.
