# Project Startup Instructions

Follow the steps below to start the necessary services for the project:
python -m pip install flask flask_cors langchain_community langchain-openai langchain-ollama langchain-chroma chromadb
---

## 1. Start Ollama

### Command to Run Ollama:

For Linux/macOS:
```bash
nohup ollama serve > ollama.log 2>&1 &
```

For Windows:
```cmd
start /b ollama serve
```

### Verify Ollama is Running:
- Open a browser or use `curl`:
  ```bash
  curl http://127.0.0.1:11434/api/version
  ```
- Check the log file (Linux/macOS):
  ```bash
  tail -f ollama.log
  ```

### Kill Ollama Process:
- Find the process ID (PID):
  ```bash
  ps aux | grep "ollama"
  ```
- Kill the process:
  ```bash
  kill <PID>
  ```
- For Windows, use Task Manager or:
  ```cmd
  taskkill /F /PID <PID>
  ```

---

## 2. Start MongoDB Locally

### Ensure MongoDB is Installed
- MongoDB must be installed and configured on your local machine.
- If not installed, follow the [MongoDB installation guide](https://www.mongodb.com/docs/manual/installation/).

### Start the MongoDB Server

For Linux/macOS:
```bash
mongod --dbpath /path/to/your/db --bind_ip 127.0.0.1 &
```

For Windows:
1. Open the Command Prompt.
2. Run:
   ```cmd
   mongod --dbpath C:\path\to\your\db --bind_ip 127.0.0.1
   ```

### Verify MongoDB is Running:
- Check the MongoDB service status using:
  ```bash
  mongo
  ```
- Use a MongoDB GUI tool like Compass if needed.

### Kill MongoDB Process:
- Find the process ID (PID):
  ```bash
  ps aux | grep "mongod"
  ```
- Kill the process:
  ```bash
  kill <PID>
  ```
- For Windows, use Task Manager or:
  ```cmd
  taskkill /F /PID <PID>
  ```

---

## 3. Start the Python Flask Server

### Prerequisites:
- Ensure Python and Flask are installed.
- If Flask is not installed, run:
  ```bash
  pip install flask
  ```

### Command to Start Flask:

For Linux/macOS:
```bash
nohup python server.py > flask_app.log 2>&1 &
```

For Windows:
1. Open the Command Prompt.
2. Run:
   ```cmd
   start /b python server.py
   ```

### Verify Flask is Running:
- Open a browser or use `curl` to check the Flask app:
  ```bash
  curl http://127.0.0.1:5000
  ```
- For Linux/macOS, monitor the log:
  ```bash
  tail -f flask_app.log
  ```

### Kill Flask Process:
- Find the process ID (PID):
  ```bash
  ps aux | grep "server.py"
  ```
- Kill the process:
  ```bash
  kill <PID>
  ```
- For Windows, use Task Manager or:
  ```cmd
  taskkill /F /PID <PID>
  ```

---

## Additional Notes:
- Use `ps aux | grep "server.py"` (Linux/macOS) or Task Manager (Windows) to find and manage running processes.
- Ensure all services are running on the expected ports:
  - Ollama: `127.0.0.1:11434`
  - MongoDB: `127.0.0.1:27017`
  - Flask: `127.0.0.1:5000`

If you encounter any issues, refer to the respective service documentation or reach out to the project maintainer.

---

### GitHub Formatting

This file is intended to be used as a GitHub `README.md`. Make sure to upload it to the root directory of your repository for proper display on GitHub.

