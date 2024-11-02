import os

from dotenv import load_dotenv
from langchain_community.embeddings import (HuggingFaceBgeEmbeddings,
                                            OpenAIEmbeddings)
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace

# Load environment variables from .env file
load_dotenv()

def get_llm(model="gpt-4o-mini"):
    if model == "gpt-4o-mini":
        api_key = os.getenv('OPENAI_API_KEY')
        return ChatOpenAI(api_key=api_key, model=model, temperature=0.1)
    elif model == "llama3.1":
        return ChatOllama(model=model, temperature=0.1, num_ctx=16384)
    elif model == "nvidia-llama3.1":
        return ChatNVIDIA(
            base_url="http://localhost:8000/v1",
            model="meta/llama-3.1-8b-instruct",
            temperature=0.1,
            max_tokens=16000
        )
    
    elif model == "hf-llama3.2":
        model = "meta-llama/Llama-3.2-3B-Instruct"

        llm = HuggingFacePipeline.from_model_id(
        model_id=model,
        task="text-generation",
        device=2,
        pipeline_kwargs=dict(
            temperature=0.1,
            max_length=16000,
        ),
        )
        llm.pipeline.tokenizer.pad_token_id = llm.pipeline.tokenizer.eos_token_id
        
        return ChatHuggingFace(llm=llm)
    
    return None

def get_embedding_model(model="text-embedding-3-small"):
    if model == "text-embedding-3-small":
        api_key = os.getenv('OPENAI_API_KEY')
        return OpenAIEmbeddings(api_key=api_key, model=model)
    elif model == "BAAI/bge-m3":
        model_kwargs = {'device': 'cuda'}
        encode_kwargs = {'normalize_embeddings': True}
        try:
            return HuggingFaceBgeEmbeddings(model_name=model, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)
        except Exception as e:
            print("Embedding using CPU due to CUDA Out of Memory!")
            model_kwargs = {'device': 'cpu'}
            return HuggingFaceBgeEmbeddings(model_name=model, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)

# Example usage
if __name__ == "__main__":
    llm = get_llm(company="azure_openai", model="gpt-35-crayon")
    print(f"LLM: {llm}")

    embedding_model = get_embedding_model(company="azure_openai", model="embedding-ada-crayon")
    print(f"Embedding Model: {embedding_model}")
