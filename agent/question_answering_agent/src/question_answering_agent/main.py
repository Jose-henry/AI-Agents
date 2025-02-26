#!/usr/bin/env python
import sys
import warnings

from pydantic import BaseModel
from datetime import datetime
from fastapi import FastAPI, HTTPException
from question_answering_agent.crew import QuestionAnsweringAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

app = FastAPI(title="Wizerly QnA Agent API")
qa_crew = QuestionAnsweringAgent().crew()

class TopicRequest(BaseModel):
    topic: str

@app.post("/run")
def run(request: TopicRequest):
    # Now we can access the "topic" from request.topic
    inputs = {"topic": request.topic}
    try:
        result = qa_crew.kickoff(inputs=inputs)
        return {"status": "success", "message": result.raw}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/train")
def train(n_iterations: int, filename: str, topic: str):
    inputs = {"topic": topic}
    try:
        qa_crew.train(n_iterations=n_iterations, filename=filename, inputs=inputs)
        return {"status": "success", "message": "Crew training completed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/test")
def test(n_iterations: int, openai_model_name: str, topic: str):
    inputs = {"topic": topic}
    try:
        qa_crew.test(n_iterations=n_iterations, openai_model_name=openai_model_name, inputs=inputs)
        return {"status": "success", "message": "Crew test executed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))