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

# TODO: parameters retriever_uu: BaseRetriever, graph_chain: GraphCypherQAChain, llm: BaseLanguageModel
def create_combined_answer_chain(retriever_uu: BaseRetriever, llm: BaseLanguageModel):
    print("A")
    CONTEXTUALIZE_Q_PROMPT = PromptTemplate.from_template(
        CONTEXTUALIZE_Q_PROMPT_STR)
    _inputs_question = CONTEXTUALIZE_Q_PROMPT | llm | StrOutputParser()
    print("B")

    question_router = question_router_chain(llm, ROUTER_PROMPT)
    QA_SYSTEM_PROMPT = PromptTemplate(input_variables=[
                                      "answer_uu", "question"], template=QA_SYSTEM_TEMPLATE_COMBINED_ANSWER)
    print("C")
    uu_chain = create_uu_chain(
        qa_system_prompt_str=QA_SYSTEM_PROMPT_UU,
        retriever=retriever_uu,
        llm=llm
    )
    print("D")

    # uu_rekam_chain = create_uu_rekam_chain(
    #     qa_system_prompt_str=QA_SYSTEM_PROMPT_UU,
    #     llm=llm,
    #     rekam_jejak_context=REKAM_JEJAK_CONTEXT,
    #     graph_chain=graph_chain,
    #     retriever=retriever_uu,
    # )

    general_chain = PromptTemplate.from_template(
        """Answer 'Saya tidak tahu' """
    ) | llm | StrOutputParser()
    print("E")

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
    print("F")

    full_chain = _inputs_question | {
        "result": question_router | StrOutputParser(),
        "question": RunnablePassthrough(),
    } | RunnablePassthrough() | RunnableBranch(
        (lambda x: "rekam_jejak" in x["result"], ketentuan_chain), # for now disable rekam chain (change to uu_rekam_chain)
        (lambda x: "ketentuan_terkait" in x["result"], ketentuan_chain),
        general_chain,
    )
    print("G")

    return full_chain