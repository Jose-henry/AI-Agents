import os
import sys
import psycopg
from psycopg2.extras import execute_values
from dotenv import load_dotenv
# Import LangChain components.
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings


# Load environment variables
load_dotenv()

def create_table(conn):
    """
    Create a table to store document chunks if it doesn't exist.
    The table contains only two columns: chunk_text and vector.
    """
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                chunk_text TEXT,
                embedding FLOAT8[]
            );
        """)
        conn.commit()

def insert_chunks(conn, chunks, embeddings):
    """
    Bulk-insert document chunks and their corresponding vector embeddings.
    Only the chunk text and vector are inserted.
    """
    with conn.cursor() as cur:
        records = [(chunk, embedding) for chunk, embedding in zip(chunks, embeddings)]
        query = "INSERT INTO documents (chunk_text, embedding) VALUES %s"
        execute_values(cur, query, records)
        conn.commit()

def main():
    if len(sys.argv) < 2:
        print("Usage: python populate_db_langchain.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Load the PDF document using LangChain's PyPDFLoader.
    print("Loading document from:", file_path)
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    if not docs:
        print("No documents loaded. Please check the file path and file format.")
        sys.exit(1)

    # Combine all page texts into one string.
    all_text = "\n".join([doc.page_content for doc in docs])
    print(f"Loaded document with {len(docs)} page(s).")

    # Split text into manageable chunks.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,        # Adjust chunk size as needed.
        chunk_overlap=200,      # Overlap helps maintain context.
        separators=["\n\n", "\n", " ", ""]
    )
    chunk_docs = text_splitter.create_documents([all_text])
    chunk_texts = [doc.page_content for doc in chunk_docs]
    print(f"Text split into {len(chunk_texts)} chunk(s).")

    # Initialize the OpenAI embeddings model.
    print("Vectorizing chunks using OpenAI embeddings...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    embeddings = embeddings.embed_documents(chunk_texts)
    print("Vectorization complete.")

    # Connect to YugabyteDB using the connection string from environment variable.
    db_url = os.getenv("YUGABYTE_DB_URL")
    if not db_url:
        print("Error: YUGABYTE_DB_URL environment variable not set.")
        sys.exit(1)

    try:
        conn = psycopg.connect(db_url)
        print("Connected to YugabyteDB.")
    except Exception as e:
        print("Error connecting to the database:", e)
        sys.exit(1)

    # Create table (if needed) and insert document chunks with their embeddings.
    create_table(conn)
    insert_chunks(conn, chunk_texts, embeddings)
    print("Document data inserted successfully into the database.")
    conn.close()

if __name__ == "__main__":
    main()
