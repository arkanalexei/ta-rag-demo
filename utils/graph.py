from SPARQLWrapper import SPARQLWrapper, TURTLE
from rdflib import Graph

def execute_construct(query, endpoint_url):
    # Initialize the SPARQL wrapper
    sparql_wrapper = SPARQLWrapper(endpoint_url)
    
    # Set the query and return format
    sparql_wrapper.setQuery(query)
    sparql_wrapper.setReturnFormat(TURTLE)
    
    # Execute the query and get the results
    results = sparql_wrapper.query().convert()
    
    res_list = []
    
    # Create an RDFLib graph and parse the results
    g = Graph()
    g.parse(data=results, format="ttl")
    
    # Extract the triples into a list
    res_list = [(str(s), str(p), str(o)) for s, p, o in g]

    return res_list