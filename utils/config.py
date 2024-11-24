import os

from dotenv import load_dotenv

load_dotenv()

def get_config():
    openai_api_key = os.getenv("OPENAI_API_KEY")

    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    cohere_api_key = os.getenv("COHERE_API_KEY")
    neo4j_uri = os.getenv("NEO4J_GRAPH_URL")
    neo4j_username = os.getenv("NEO4J_USERNAME")
    neo4j_password = os.getenv("NEO4J_PASSWORD")
    neo4j_db = os.getenv("NEO4J_DATABASE")

    graphdb_uri = os.getenv("GRAPHDB_URL")


    return {
        "openai_api_Key": openai_api_key,
        "pinecone_api_key": pinecone_api_key,
        "cohere_api_key": cohere_api_key,
        "neo4j_uri": neo4j_uri,
        "neo4j_username": neo4j_username,
        "neo4j_password": neo4j_password,
        "neo4j_db": neo4j_db,
        "graphdb_uri": graphdb_uri,
    }