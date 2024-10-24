import json
from operator import itemgetter

from langchain.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import (RunnableBranch, RunnableLambda,
                                      RunnablePassthrough)

from utils.chain.routing import question_router_chain
from utils.chain.uu.chain_uu import create_uu_chain, create_uu_rekam_chain
from utils.prompt.main import (CONTEXTUALIZE_Q_PROMPT_STR, QA_SYSTEM_PROMPT_UU,
                               QA_SYSTEM_TEMPLATE_COMBINED_ANSWER,
                               REKAM_JEJAK_CONTEXT)
from utils.prompt.routing import ROUTER_PROMPT


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

    question_router = question_router_chain(llm, ROUTER_PROMPT)
    QA_SYSTEM_PROMPT = PromptTemplate(input_variables=[
                                      "answer_uu", "question"], template=QA_SYSTEM_TEMPLATE_COMBINED_ANSWER)
    
    uu_chain = create_uu_chain(
        qa_system_prompt_str=QA_SYSTEM_PROMPT_UU,
        retriever=retriever_uu,
        llm=llm
    )

    uu_rekam_chain = create_uu_rekam_chain(
        qa_system_prompt_str=QA_SYSTEM_PROMPT_UU,
        llm=llm,
        rekam_jejak_context=REKAM_JEJAK_CONTEXT,
        graph_chain=graph_chain,
        retriever=retriever_uu,
    )

    general_chain = PromptTemplate.from_template(
        """Answer 'Saya tidak tahu' """
    ) | llm | StrOutputParser()

    ketentuan_chain = RunnablePassthrough() | {"question": itemgetter("question")} | {
        "chain_uu":   uu_chain,
        "question":   itemgetter("question")
    } | {
        "answer_uu":   itemgetter("chain_uu") | RunnablePassthrough() | itemgetter("answer") | RunnablePassthrough(),
        "context_uu":   itemgetter("chain_uu") | RunnablePassthrough() | itemgetter("context") | RunnablePassthrough(),
        "question":   itemgetter("question")
    } | {
        "rewrited question":   itemgetter("question"),
        "context":   RunnableLambda(merge_context),
        "context_text": RunnableLambda(merge_answer),
        "answer":   QA_SYSTEM_PROMPT | llm | StrOutputParser()
    }

    full_chain = _inputs_question | {
        "question": RunnablePassthrough(),
    } | RunnablePassthrough() | uu_rekam_chain

    return full_chain