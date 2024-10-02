from langchain.retrievers.merger_retriever import MergerRetriever
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain.retrievers.document_compressors.base import \
    DocumentCompressorPipeline
from langchain_community.cross_encoders.huggingface import HuggingFaceCrossEncoder
from langchain_community.document_transformers import (
    EmbeddingsRedundantFilter, LongContextReorder)
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.runnables import RunnableLambda
from langchain_core.vectorstores import VectorStore

from utils.retriever.self_query import to_documents
from utils.retriever.uu.self_query_uu import self_query_uu


def get_embedding_uu(vector_store: VectorStore, llm: BaseLanguageModel, embed_model: Embeddings, top_k: int = 8, with_self_query: bool = True):
    #retriever_self_query_mmr = self_query_uu(
    #    llm=llm,
    #    vector_store=vector_store,
    #    search_type="mmr",
    #)

    retriever_similarity = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={'k': top_k}
    )
    retriever_mmr = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={'k': top_k, 'lambda_mult': 0.85, 'fetch_k': 40}
    )

    lotr = retriever_mmr
    # merge retrievers
    if with_self_query:
        lotr = MergerRetriever(retrievers=[retriever_self_query_mmr, retriever_similarity])

    # reranker
    model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-v2-m3")
    cross_encoder_compressor = CrossEncoderReranker(model=model, top_n=top_k)
    reranked_retriever = ContextualCompressionRetriever(
        base_compressor=cross_encoder_compressor, base_retriever=lotr
    )

    # remove redundant documents
    filter = EmbeddingsRedundantFilter(embeddings=embed_model)
    reordering = LongContextReorder()
    pipeline = DocumentCompressorPipeline(transformers=[filter, reordering])
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=pipeline, base_retriever=reranked_retriever
    )

    chain = compression_retriever | RunnableLambda(to_documents)

    return chain
