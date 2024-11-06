from langchain.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import RunnablePassthrough

from utils.chain.uu.chain_uu import create_uu_rekam_chain
from utils.prompt.main import (CONTEXTUALIZE_Q_PROMPT_STR, QA_SYSTEM_PROMPT_UU_COT,
                               REKAM_JEJAK_CONTEXT)


def merge_context(results):
    merged = results["context_uu"]
    return merged

def merge_answer(results):
    merged = [results["answer_uu"]]
    return merged

def create_combined_answer_chain(retriever_uu: BaseRetriever, graph_chain: GraphCypherQAChain, llm: BaseLanguageModel):
    CONTEXTUALIZE_Q_PROMPT = PromptTemplate.from_template(
        CONTEXTUALIZE_Q_PROMPT_STR)
    _inputs_question = CONTEXTUALIZE_Q_PROMPT | llm | StrOutputParser()

    uu_rekam_chain = create_uu_rekam_chain(
        qa_system_prompt_str=QA_SYSTEM_PROMPT_UU_COT,
        llm=llm,
        rekam_jejak_context=REKAM_JEJAK_CONTEXT,
        graph_chain=graph_chain,
        retriever=retriever_uu,
    )

    full_chain = _inputs_question | {
        "question": RunnablePassthrough(),
    } | RunnablePassthrough() | uu_rekam_chain

    return full_chain