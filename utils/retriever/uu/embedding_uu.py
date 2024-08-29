from langchain.retrievers import (ContextualCompressionRetriever,
                                  MergerRetriever)
from langchain.retrievers.document_compressors.base import \
    DocumentCompressorPipeline
from langchain_community.document_transformers import (
    EmbeddingsRedundantFilter, LongContextReorder)
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.runnables import RunnableLambda
from langchain_core.vectorstores import VectorStore

from utils.retriever.self_query import to_documents
from utils.retriever.uu.self_query_uu import self_query_uu


def get_embedding_uu(vector_store: VectorStore, llm: BaseLanguageModel, embed_model: Embeddings, top_k: int = 8, with_self_query: bool = True):
    retriever_self_query_mmr = self_query_uu(
        llm=llm,
        vector_store=vector_store,
        search_type="mmr",
    )

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

    # remove redundant documents
    filter = EmbeddingsRedundantFilter(embeddings=embed_model)
    # reordering = LongContextReorder()
    pipeline = DocumentCompressorPipeline(transformers=[filter])
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=pipeline, base_retriever=lotr
    )

    chain = compression_retriever | RunnableLambda(to_documents)

    return chain
