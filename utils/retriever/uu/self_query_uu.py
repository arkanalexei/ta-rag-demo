from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.vectorstores import VectorStore
from utils.retriever.self_query import self_query

# Define metadata field information
metadata_field_info = [
    AttributeInfo(
        name="nomor",
        description="The number of the regulation (nomor ketentuan, nomor regulasi, nomor peraturan)",
        type="string",
    ),
    # AttributeInfo(
    #     name="tahun",
    #     description="The year of the regulation (tahun ketentuan, tahun regulasi, tahun peraturan)",
    #     type="string",
    # ),
    AttributeInfo(
        name="jenis_bentuk_peraturan",
        description="The type of the regulation (jenis bentuk ketentuan, jenis bentuk regulasi, jenis bentuk peraturan)",
        type="string",
    ),
    # TODO: field ditetapkan_tanggal
]

# Define document content description
document_content_description = "The content of the document"


def self_query_uu(llm: BaseLanguageModel, vector_store: VectorStore, search_type: str = "similarity") -> SelfQueryRetriever:
    return self_query(llm, vector_store, document_content_description, metadata_field_info, search_type=search_type)
