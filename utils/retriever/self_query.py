from typing import Sequence, Union

from langchain.chains.query_constructor.base import (
    AttributeInfo, StructuredQueryOutputParser, get_query_constructor_prompt)
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_community.document_transformers.embeddings_redundant_filter import \
    _DocumentWithState
from langchain_community.query_constructors.qdrant import QdrantTranslator
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.prompts import BasePromptTemplate
from langchain_core.vectorstores import VectorStore

from utils.prompt.self_query import DEFAULT_SCHEMA_PROMPT


def to_documents(context: list[_DocumentWithState]):
    context_unique = [i.to_document() for i in context]
    return context_unique

def self_query(llm_model: BaseLanguageModel, vector_store: VectorStore, document_content_description: str, metadata_field_info: Sequence[Union[AttributeInfo, dict]], search_type: str = "similarity", schema_prompt: BasePromptTemplate = DEFAULT_SCHEMA_PROMPT, top_k: int = 8) -> SelfQueryRetriever:
    translator = QdrantTranslator(metadata_key="metadata")
    prompt = get_query_constructor_prompt(
        document_contents=document_content_description,
        attribute_info=metadata_field_info,
        schema_prompt=schema_prompt,
        allowed_comparators=translator.allowed_comparators,
        allowed_operators=translator.allowed_operators
    )

    output_parser = StructuredQueryOutputParser.from_components()
    query_constructor = prompt | llm_model | output_parser

    retriever = SelfQueryRetriever(
        query_constructor=query_constructor,
        vectorstore=vector_store,
        search_type=search_type,
        search_kwargs={'k': top_k}
    )

    if search_type == "mmr":
        retriever = SelfQueryRetriever(
        query_constructor=query_constructor,
        vectorstore=vector_store,
        search_type=search_type,
        search_kwargs={'k': top_k, 'lambda_mult': 0.85, 'fetch_k': 40}
    )

    return retriever