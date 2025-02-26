#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from retrieval_agent.crew import RetrievalAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally. Replace with inputs you want to test; it will automatically
# interpolate any tasks and agents information.

app = FastAPI(title="Wizerly Retrieval Agent API")
retrieval_crew = RetrievalAgent().crew()

class TopicRequest(BaseModel):
    topic: str

@app.post("/run")
def run(request: TopicRequest):
    inputs = {
        "topic": request.topic,
        "current_year": str(datetime.now().year)
    }
    try:
        retrieval_crew.kickoff(inputs=inputs)
        # For simplicity, we assume the retrieval task returns context based on the topic.
        return {"status": "success", "message": f"Retrieved context for query: {request.topic}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/train")
def train(n_iterations: int, filename: str, request: TopicRequest):
    inputs = {"topic": request.topic}
    try:
        retrieval_crew.train(n_iterations=n_iterations, filename=filename, inputs=inputs)
        return {"status": "success", "message": "Retrieval crew training completed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/test")
def test(n_iterations: int, openai_model_name: str, request: TopicRequest):
    inputs = {"topic": request.topic}
    try:
        retrieval_crew.test(n_iterations=n_iterations, openai_model_name=openai_model_name, inputs=inputs)
        return {"status": "success", "message": "Retrieval crew test executed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
