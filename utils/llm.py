import os

from dotenv import load_dotenv
from langchain_community.embeddings import (HuggingFaceBgeEmbeddings,
                                            OpenAIEmbeddings)
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace

import torch
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import torch.nn.functional as F
from sklearn.preprocessing import normalize

# Load environment variables from .env file
load_dotenv()

def get_llm(model="gpt-4o-mini", temperature=0.5, top_p=0.5):
    if model == "gpt-4o-mini":
        api_key = os.getenv('OPENAI_API_KEY')
        return ChatOpenAI(api_key=api_key, model=model, temperature=0.1)
    elif model == "llama3.1":
        return ChatOllama(model=model, temperature=0.1, num_ctx=16384)
    elif model == "nvidia-llama3.1":
        return ChatNVIDIA(
            base_url="http://localhost:8000/v1",
            model="meta/llama-3.1-8b-instruct",
            temperature=temperature,
            top_p=top_p,
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
    elif model == "hf-qwen-coder2.5":
        model = "Qwen/Qwen2.5-Coder-7B-Instruct"

        llm = HuggingFacePipeline.from_model_id(
        model_id=model,
        task="text-generation",
        device=0,
        pipeline_kwargs=dict(
            temperature=0.5,
            max_length=16000,
        ),
        )

        llm.pipeline.tokenizer.pad_token_id = llm.pipeline.tokenizer.eos_token_id
        return ChatHuggingFace(llm=llm)
    
    return None

def get_embedding_model(model="text-embedding-3-small"):
    """
    Returns an embedding model instance based on the specified model name.
    """
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

    elif model == "nvidia/NV-Embed-v2":
        def nv_embed_model(queries, passages, max_length=32768, batch_size=32):
            # Task-specific prefixes
            query_prefix = "Instruct: Given a question, retrieve passages that answer the question\nQuery: "
            passage_prefix = ""

            # Load the model and tokenizer
            embedding_model = AutoModel.from_pretrained('nvidia/NV-Embed-v2', trust_remote_code=True).cuda()
            tokenizer = AutoTokenizer.from_pretrained('nvidia/NV-Embed-v2', trust_remote_code=True)

            # Process queries
            query_inputs = tokenizer([query_prefix + q for q in queries], truncation=True, padding=True,
                                      return_tensors="pt", max_length=max_length).to("cuda")
            query_embeddings = embedding_model(**query_inputs).last_hidden_state.mean(dim=1)
            query_embeddings = F.normalize(query_embeddings, p=2, dim=1)

            # Process passages
            passage_inputs = tokenizer(passages, truncation=True, padding=True, return_tensors="pt",
                                        max_length=max_length).to("cuda")
            passage_embeddings = embedding_model(**passage_inputs).last_hidden_state.mean(dim=1)
            passage_embeddings = F.normalize(passage_embeddings, p=2, dim=1)

            return query_embeddings, passage_embeddings

        return nv_embed_model

    elif model == "dunzhang/stella_en_1.5B_v5":
        def stella_model(queries, docs, vector_dim=1024):
            # Task-specific prefixes
            query_prompt_name = "s2p_query"

            # Load the model
            embedding_model = SentenceTransformer("dunzhang/stella_en_1.5B_v5", trust_remote_code=True).cuda()
            embedding_model.max_seq_length = 512

            # Encode queries and documents
            query_embeddings = embedding_model.encode(queries, prompt_name=query_prompt_name)
            doc_embeddings = embedding_model.encode(docs)

            return query_embeddings, doc_embeddings

        return stella_model

    else:
        raise ValueError(f"Model {model} is not supported.")

# Example usage
if __name__ == "__main__":
    llm = get_llm(company="azure_openai", model="gpt-35-crayon")
    print(f"LLM: {llm}")

    embedding_model = get_embedding_model(company="azure_openai", model="embedding-ada-crayon")
    print(f"Embedding Model: {embedding_model}")
