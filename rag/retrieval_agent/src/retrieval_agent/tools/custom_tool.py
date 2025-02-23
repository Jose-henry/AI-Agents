import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text
from langchain_postgres.vectorstores import PGVector
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# Retrieve the connection string from environment variables
connection_string = os.getenv(
    "YUGABYTE_DB_URL",
    "postgresql+psycopg://yugabyte:@localhost:5433/yugabyte?sslmode=disable"
)

# Create engine
engine = create_engine(connection_string)

# Set the YugabyteDB flag before initializing PGVector
with engine.connect() as connection:
    connection.execute(text("SET yb_silence_advisory_locks_not_supported_error = on;"))
    connection.commit()

# Initialize the OpenAI embeddings model
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

# Initialize the PGVector store
pgvector_store = PGVector(
    embeddings=embedding_model,
    collection_name="documents",
    connection=engine,
    use_jsonb=True,
)

class PGVectorToolInput(BaseModel):
    query: str = Field(..., description="The query text for vector similarity search.")

class PGVectorTool(BaseTool):
    name: str = "PGVectorTool"
    description: str = (
        "Performs a vector similarity search on the 'documents' collection using PGVector from langchain_postgres."
    )
    args_schema: Type[BaseModel] = PGVectorToolInput

    def _run(self, query: str) -> str:
        results = pgvector_store.similarity_search(query, k=5)
        return "\n".join([str(result) for result in results])