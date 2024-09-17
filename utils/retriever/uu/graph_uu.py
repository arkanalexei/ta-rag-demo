from langchain.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.prompts import PromptTemplate

from utils.database.neo4j import Neo4jGraphStore
from utils.prompt.graph import GRAPH_CYPHER_GEN_PROMPT, GRAPH_QA_GEN_PROMPT


def get_graph_uu(llm: BaseLanguageModel, config: dict):
    neo4j_sikepo = Neo4jGraphStore(config=config)
    graph = neo4j_sikepo.get_graph()

    qa_generation_template = GRAPH_QA_GEN_PROMPT
    qa_generation_prompt = PromptTemplate(
        input_variables=["context", "question"], template=qa_generation_template)

    cypher_generation_template = GRAPH_CYPHER_GEN_PROMPT
    cypher_generation_prompt = PromptTemplate(input_variables=["schema", "question"], template=cypher_generation_template)

    chain = GraphCypherQAChain.from_llm(
        cypher_llm=llm, qa_llm=llm, graph=graph, verbose=True, validate_cypher=True, qa_prompt=qa_generation_prompt, cypher_prompt=cypher_generation_prompt, allow_dangerous_requests=True
    )

    return chain

