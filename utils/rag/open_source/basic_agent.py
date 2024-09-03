import os

from langchain.chains.conversational_retrieval.base import \
    ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors.flashrank_rerank import \
    FlashrankRerank
from langchain_qdrant import QdrantVectorStore

from utils.database.qdrant import QdrantIndexManager
from utils.llm import get_embedding_model, get_llm
from utils.prompt.main import MAIN_SYSTEM_PROMPT
from utils.rag.helpers import (format_sources, get_user_memory,
                               is_answer_uncertain)
from utils.utils import is_language_indonesian, translate


llm = get_llm(model="llama3.1")
embed_model = get_embedding_model(model="BAAI/bge-m3")
vectorstore = QdrantIndexManager(embed_model=embed_model, index_name="uu").load_vector_index()
retriever = vectorstore.as_retriever(search_kwargs={"k": 15})

def get_qa_chain(user_id):
    # Custom prompt template
    PROMPT = PromptTemplate(
        input_variables=["context", "chat_history", "question"],
        template=MAIN_SYSTEM_PROMPT
    )

    # Get or create the user's memory
    memory = get_user_memory(user_id, llm)

    # Create the conversational chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={
            "prompt": PROMPT,
            "document_variable_name": "context",
            },
        return_source_documents=True,
        max_tokens_limit=16384
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


def caller_with_sources(question, user_id):
    qa_chain = get_qa_chain(user_id)

    result = qa_chain({"question": question})
    answer = result['answer']

    # if is_answer_uncertain(answer, llm_model="llama3.1"):
    #     return answer, result["source_documents"]

    return answer, result["source_documents"]