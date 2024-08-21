import os

from langchain.chains.conversational_retrieval.base import \
    ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.retrievers import (ContextualCompressionRetriever,
                                  MergerRetriever, MultiQueryRetriever,
                                  ParentDocumentRetriever)
from langchain.retrievers.document_compressors.flashrank_rerank import \
    FlashrankRerank
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore

from utils.llm import get_embedding_model, get_llm
from utils.prompt.main import MAIN_SYSTEM_PROMPT
from utils.rag.helpers import (format_sources, get_docstore, get_user_memory,
                               is_answer_uncertain)
from utils.utils import is_language_indonesian, translate


def get_qa_chain(user_id):
    llm = get_llm(model="llama3.1")
    embed_model = get_embedding_model(model="BAAI/bge-m3")

    vectorstore = QdrantVectorStore.from_existing_collection(collection_name="uu", embedding=embed_model, path="qdrant")

    multi_query_retriever = MultiQueryRetriever.from_llm(
        retriever=vectorstore.as_retriever(search_kwargs={"k": 10}),
        llm=llm
    )

    docstore = get_docstore()

    child_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=200)

    parent_retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=docstore,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter,
        search_kwargs={"k": 30}
    )

    # Use MergerRetriever to combine results from both retrievers
    merger_retriever = MergerRetriever(retrievers=[multi_query_retriever, parent_retriever])

    compressor = FlashrankRerank(top_n=15, model="ms-marco-MultiBERT-L-12")
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=merger_retriever
    )

    PROMPT = PromptTemplate(
        input_variables=["context", "chat_history", "question"],
        template=MAIN_SYSTEM_PROMPT
    )

    memory = get_user_memory(user_id)

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=compression_retriever,
        memory=memory,
        combine_docs_chain_kwargs={
            "prompt": PROMPT,
            "document_variable_name": "context",
            },
        return_source_documents=True,
        max_tokens_limit=4000
    )
    return qa_chain

def caller(question, user_id):
    qa_chain = get_qa_chain(user_id)
    # is_indonesian = is_language_indonesian(question)

    # if is_indonesian:
    #     question = translate("en", question)

    result = qa_chain({"question": question})
    answer = result['answer']

    # if is_indonesian:
    #     answer = translate("id", answer)

    if is_answer_uncertain(answer, llm_model="llama3.1"):
        return answer

    formatted_sources = format_sources(result['source_documents'])
    return f"{answer}\n\n\nSources:\n\n{formatted_sources}"