from langchain.chains.graph_qa.cypher import GraphCypherQAChain
from langchain.chains import OntotextGraphDBQAChain
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.prompts import PromptTemplate

from utils.database.neo4j import Neo4jGraphStore
from utils.database.graphdb import GraphDBStore
from utils.prompt.graph import *

from utils.chain.custom_graphdb import CustomOntotextGraphDBQAChain


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

def get_graph_from_graphdb_uu(llm: BaseLanguageModel, config: dict, sparql_k: int = 0):
    shot_map = {
        0: GRAPH_SPARQL_GEN_0_SHOT_PROMPT,
        1: GRAPH_SPARQL_GEN_1_SHOT_PROMPT,
        3: GRAPH_SPARQL_GEN_3_SHOT_PROMPT,
        # to be added another k-shot prompt
    }
    
    graphdb = GraphDBStore(config=config)
    graph = graphdb.get_graph()

    qa_generation_template = GRAPH_SPARQL_QA_GEN_PROMPT
    qa_prompt = PromptTemplate(
        input_variables=["context", "prompt"], template=qa_generation_template)

    sparql_generation_template = shot_map[sparql_k]
    sparql_generation_prompt = PromptTemplate(input_variables=["prompt", "schema"], template=sparql_generation_template)

    chain = OntotextGraphDBQAChain.from_llm(
        llm=llm, graph=graph, verbose=True, sparql_generation_prompt=sparql_generation_prompt, max_fix_retries=5, qa_prompt=qa_prompt, allow_dangerous_requests=True
    )
    
    # chain = OntotextGraphDBQAChain.from_llm(
    #     llm=llm, graph=graph, verbose=True, sparql_generation_prompt=sparql_generation_prompt, max_fix_retries=5, qa_prompt=None, allow_dangerous_requests=True
    # )

    return chain

def get_prompt_template(sparql_k: int, query_type: str, is_cot: bool):
    shot_map = {
        (0, "construct", False): CONSTRUCT_SPARQL_GEN_0_SHOT_PROMPT,
        (1, "construct", False): CONSTRUCT_SPARQL_GEN_1_SHOT_PROMPT,
        (2, "construct", False): CONSTRUCT_SPARQL_GEN_2_SHOT_PROMPT,
        (3, "construct", False): CONSTRUCT_SPARQL_GEN_3_SHOT_PROMPT,
        (4, "construct", False): CONSTRUCT_SPARQL_GEN_4_SHOT_PROMPT,
        (5, "construct", False): CONSTRUCT_SPARQL_GEN_5_SHOT_PROMPT,
        (0, "select", False): SELECT_SPARQL_GEN_0_SHOT_PROMPT,
        (1, "select", False): SELECT_SPARQL_GEN_1_SHOT_PROMPT,
        (2, "select", False): SELECT_SPARQL_GEN_2_SHOT_PROMPT,
        (3, "select", False): SELECT_SPARQL_GEN_3_SHOT_PROMPT,
        (4, "select", False): SELECT_SPARQL_GEN_4_SHOT_PROMPT,
        (5, "select", False): SELECT_SPARQL_GEN_5_SHOT_PROMPT,
        (0, "construct", True): CONSTRUCT_SPARQL_GEN_COT_0_SHOT_PROMPT,
        (1, "construct", True): CONSTRUCT_SPARQL_GEN_COT_1_SHOT_PROMPT,
        (2, "construct", True): CONSTRUCT_SPARQL_GEN_COT_2_SHOT_PROMPT,
        (3, "construct", True): CONSTRUCT_SPARQL_GEN_COT_3_SHOT_PROMPT,
        (4, "construct", True): CONSTRUCT_SPARQL_GEN_COT_4_SHOT_PROMPT,
        (5, "construct", True): CONSTRUCT_SPARQL_GEN_COT_5_SHOT_PROMPT,
        (0, "select", True): SELECT_SPARQL_GEN_COT_0_SHOT_PROMPT,
        (1, "select", True): SELECT_SPARQL_GEN_COT_1_SHOT_PROMPT,
        (2, "select", True): SELECT_SPARQL_GEN_COT_2_SHOT_PROMPT,
        (3, "select", True): SELECT_SPARQL_GEN_COT_3_SHOT_PROMPT,
        (4, "select", True): SELECT_SPARQL_GEN_COT_4_SHOT_PROMPT,
        (5, "select", True): SELECT_SPARQL_GEN_COT_5_SHOT_PROMPT,
        # add prompt for another scenario
    }
    return shot_map[(sparql_k, query_type, is_cot)]

def get_graph_from_custom_graphdb_uu(llm: BaseLanguageModel, config: dict, sparql_k: int = 0, query_type: str = "construct", is_cot: bool = False):
    
    graphdb = GraphDBStore(config=config)
    graph = graphdb.get_graph()

    qa_generation_template = GRAPH_SPARQL_QA_GEN_PROMPT
    qa_prompt = PromptTemplate(
        input_variables=["context", "prompt"], template=qa_generation_template)

    sparql_generation_template = get_prompt_template(sparql_k=sparql_k, query_type=query_type, is_cot=is_cot)
    sparql_generation_prompt = PromptTemplate(input_variables=["prompt", "schema"], template=sparql_generation_template)

    chain = CustomOntotextGraphDBQAChain.from_llm(
        llm=llm, graph=graph, verbose=True, sparql_generation_prompt=sparql_generation_prompt, max_fix_retries=0, qa_prompt=qa_prompt, allow_dangerous_requests=True
    )
    
    # chain = CustomOntotextGraphDBQAChain.from_llm(
    #     llm=llm, graph=graph, verbose=True, sparql_generation_prompt=sparql_generation_prompt, max_fix_retries=5, qa_prompt=None, allow_dangerous_requests=True
    # )

    return chain

