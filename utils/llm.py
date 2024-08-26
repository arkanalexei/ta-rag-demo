import os

from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI, ChatOllama
from langchain_community.embeddings import OpenAIEmbeddings, HuggingFaceBgeEmbeddings

# Load environment variables from .env file
load_dotenv()

def get_llm(model="gpt-4o-mini"):
    if model == "gpt-4o-mini":
        api_key = os.getenv('OPENAI_API_KEY')
        return ChatOpenAI(api_key=api_key, model=model, temperature=0.1)
    elif model == "llama3.1":
        return ChatOllama(model=model, temperature=0.1)
    
    return llm

def get_embedding_model(model="text-embedding-3-small"):
    if model == "text-embedding-3-small":
        api_key = os.getenv('OPENAI_API_KEY')
        return OpenAIEmbeddings(api_key=api_key, model=model)
    elif model == "BAAI/bge-m3":
        model_kwargs = {'device': 'cuda'}
        encode_kwargs = {'normalize_embeddings': True}
        return HuggingFaceBgeEmbeddings(model_name=model, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)    

# Example usage
if __name__ == "__main__":
    llm = get_llm(company="azure_openai", model="gpt-35-crayon")
    print(f"LLM: {llm}")

    embedding_model = get_embedding_model(company="azure_openai", model="embedding-ada-crayon")
    print(f"Embedding Model: {embedding_model}")
