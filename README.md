# Multi-Agent QnA and RAG Implementation with CrewAI

## Overview
This project implements a microservice-based AI system using **CrewAI**, designed for Question & Answer (QnA) and Retrieval-Augmented Generation (RAG). The architecture consists of two primary AI agents:

1. **QnA Agent** – Handles user interactions, processes queries, and retrieves relevant information.
2. **RAG Agent** – Performs retrieval-based tasks to fetch relevant documents for QnA processing.

Both agents are deployed with **YugaByteDB** for efficient storage and retrieval.

---

## Project Structure
```
/multi-agent-qna
│
├── /agent
│   ├── question_answering_agent/
|            ├── QnA_configuration.yaml
│            └── src/
│
├── /rag
│   ├── retrieval_agent/
│            ├── rag_configuration.yaml
│            ├── populate_db_langchain.py  # Script to populate the database with PDF content
│            └── src/
│
│
└── README.md
---

## Deployment Methods
### Method 1: Running with Uvicorn (Local Development)
To start the services manually using **Uvicorn**, follow these steps:

1. Navigate to the `src` directory of the QnA agent and start the server:
   ```bash
   cd agent/.../src
   uvicorn question_answering_agent.main:app --reload --port 8000
   ```
2. Open a new terminal and navigate to the `src` directory of the RAG agent:
   ```bash
   cd rag/.../src
   uvicorn retrieval_agent.main:app --reload --port 8001
   ```
Ensure all required environment variables are set and the database is connected.

---

### Method 2: Running with Docker
For containerized deployment, follow these steps:

1. Build and run the **QnA agent**:
   ```bash
   cd agent/.../question_answering_agent
   docker build -t question-answering-agent:1.0 .
   docker run --env-file .env --name QnA-agent -p 8000:8000 -d question-answering-agent:1.0
   ```
2. Build and run the **RAG agent**:
   ```bash
   cd rag/.../retrieval_agent
   docker build -t retrieval-agent:1.0 .
   docker run --env-file .env --name rag-agent -p 8001:8001 -d retrieval-agent:1.0
   ```
Ensure `.env` files contain the necessary configuration.

---

### Method 3: Running with Kubernetes (Minikube)
For Kubernetes deployment, follow these steps:

1. Install **Kubectl** and **Minikube** and start the cluster:
   ```bash
   minikube start
   ```
2. Deploy **YugaByteDB** in the Kubernetes cluster:
   ```bash
  Using **HELM** or any other supported package manager for minikube cluster
   ```
3. Deploy microservices using Kubernetes configuration files:
   ```bash
   kubectl apply -f QnA_configuration.yaml
   kubectl apply -f rag_configuration.yaml
   ```
4. Forward ports for testing:
   ```bash
   kubectl --namespace yb-demo port-forward svc/yb-tserver-service 5433:5433
   ```
   
📌 **References:**
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/handbook/pushing/#Linux)
- [Minikube Installation](https://k8s-docs.netlify.app/en/docs/tasks/tools/install-minikube/)
- [YugaByte Installation & Deployment](https://download.yugabyte.com/local#kubernetes)

---

## Database Population
To populate the database with a PDF file, use the following command:
```bash
python populate_db_langchain.py '<PDF_PATH>'
```
Ensure the database is running before executing this script.

---

## API Endpoint
Once both services are running, you can interact with the system using the following endpoint:

- **Endpoint:** `http://localhost:8000/run`
- **Request Payload:**
  ```json
  {
    "topic": "Tell me about the uploaded PDF"
  }
  ```
- **Expected Response:** AI-generated response based on the content retrieved by the RAG agent.

---

## Conclusion
This multi-agent system is designed to enhance document-based QnA interactions using a robust retrieval pipeline powered by YugaByteDB, CrewAI, and Minikube for scalable deployment. Whether you prefer running the application locally, in Docker containers, or on Kubernetes, this guide provides a structured approach for implementation.

For any issues or contributions, please refer to the project repository.

🚀 **Happy Coding!**

