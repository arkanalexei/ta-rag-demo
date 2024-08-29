from typing import Literal

from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnableLambda

from utils.prompt.routing import KETENTUAN_ANSWERING_PROMPT, ROUTER_PROMPT


class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["rekam_jejak", "ketentuan_terkait", ] = Field(
        ...,
        description="Given a user question choose which datasource would be most relevant for answering their question",
    )


class RouteQueryAnswer(BaseModel):
    """Route an LLM Response whether it is answering the question or not."""

    decision: Literal["YES", "NO", ] = Field(
        ...,
        description="Given an LLM Response to the Question, choose whether the response is answering the question or NOT answering the question",
    )


def get_string_routing(route):
    return route.datasource


def get_string_answer(route):
    return route.decision


def question_router_chain(llm: BaseLanguageModel, ROUTING_PROMPT: str = ROUTER_PROMPT):
    structured_llm = llm.with_structured_output(RouteQuery)
    system = ROUTING_PROMPT
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "{question}"),
        ]
    )

    # Define router
    router = prompt | structured_llm | RunnableLambda(get_string_routing)
    return router


def ketentuan_router_chain(llm: BaseLanguageModel, ROUTING_PROMPT: str = KETENTUAN_ANSWERING_PROMPT):
    structured_llm = llm.with_structured_output(RouteQueryAnswer)
    system = ROUTING_PROMPT
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "{question}"),
            ("ai", "{answer}")
        ]
    )

    # Define router
    router = prompt | structured_llm | RunnableLambda(get_string_answer)
    return router
