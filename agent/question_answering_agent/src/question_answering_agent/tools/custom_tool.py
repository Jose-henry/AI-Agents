import os
import requests
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from dotenv import load_dotenv


load_dotenv()
class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Query text.")

class MyCustomTool(BaseTool):
    name: str = "RAG Delegator"
    description: str = (
        "Delegates retrieval of relevant Wizerly context to the RAG agent via HTTP call."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # If the query is not about Wizerly, return "I don't know"
        # if "wizerly" not in argument.lower():
        #     return "I don't know"
        
        # Get the RAG agent URL from the environment
        rag_url = os.getenv("RAG_AGENT_URL")
        if not rag_url:
            return "RAG agent URL not provided in environment variables."
        
        try:
            payload = {"topic": argument}
            response = requests.post(f"{rag_url}/run", json=payload)
            response.raise_for_status()
            data = response.json()
            # We assume the RAG agent returns a JSON response with a "message" field containing context.
            context = data.get("message", "No context returned.")
            return context
        except Exception as e:
            return f"Error calling RAG agent: {str(e)}"
