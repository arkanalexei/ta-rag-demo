from SPARQLWrapper import SPARQLWrapper, TURTLE, JSON
from rdflib import Graph
import re
import os
import pickle
from utils.utils import load_from_pickle, save_to_pickle

###########################################################################
# HELPER FUNCTION
###########################################################################

def tokenize_where_body(query: str):
    tokens = []
    where_clause_match = re.search(r"WHERE\s*{(.*)}", query, re.DOTALL)
    if where_clause_match:
        where_clause = where_clause_match.group(1).strip()

        # Tokenize WHERE clause (keeping semicolons, dots, commas)
        tokens = re.findall(r'\?[a-zA-Z_:<>/.#-]+|[a-zA-Z_:<>/.#-]+|"[^"]+"|;|\.|,', where_clause)

    #     print("Tokens in WHERE clause:", tokens)
    # else:
    #     print("Cannot find any tokens in WHERE body")
    
    return tokens

def extract_variables(query: str):
    # Extract variables in the SELECT clause
    variables = []
    select_variables = re.findall(r"SELECT\s+(.*?)\s+WHERE", query, re.DOTALL)
    if select_variables:
        variables = select_variables[0].split()
        # print("Variables in SELECT clause:", variables)
    # else:
        # print("Can't find any variables in the SELECT clause")
    
    return variables

def filter_triples(triples: list[tuple], query: str):
    vars = extract_variables(query)
    return [triple for triple in triples if triple[0] in vars or triple[2] in vars]

def expand_prefixed_iri(tokens: list[str]):
    PREFIX_MAP = {
        "rdfs"      : "http://www.w3.org/2000/01/rdf-schema#",
        "rdf"       : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "lexid"     : "https://w3id.org/lex-id/data/",
        "lexid-s"   : "https://w3id.org/lex-id/schema/",
        "xsd"       : "http://www.w3.org/2001/XMLSchema#" ,
        "dbo"       : "http://dbpedia.org/ontology/",
        "dct"       : "http://purl.org/dc/terms/",
        "owl"       : "http://www.w3.org/2002/07/owl#",
        "wd"        : "https://www.wikidata.org/wiki/",
    }

    output_lst = list()
    for token in tokens:
        if ":" not in token:
            output_lst.append(token)
            continue
        prefix, name = token.split(":", 1)
        if prefix in PREFIX_MAP:
            output_lst.append(PREFIX_MAP[prefix] + name)
            continue
        output_lst.append(token) # If there is no supported prefix
    
    return output_lst

def extract_triples_from_query(query):
    tokens = tokenize_where_body(query)
    tokens = [t if t != "a" else "rdf:type" for t in tokens]
    tokens = [t for t in tokens if not t.isupper()] # filter keywords
    tokens = expand_prefixed_iri(tokens)
    
    s, p = None, None
    triples = list()

    for token in tokens:
        if token == ',':  # Continue to the next object for the same subject
            continue
        elif token == ";": # Continue to the next predicate for the same subject
            p = None
        elif token == '.':  # End of a statement
            s = None
            p = None
        elif s is None:  # Set the subject if it's not already set
            s = token
        elif p is None:  # Set the predicate if it's not already set
            p = token
        else:  # The token is the object
            triples.append((s, p, token))

    return triples

def extract_triples(query: str):
    triples = extract_triples_from_query(query)
    filtered_triples = filter_triples(triples, query)

    return filtered_triples

###########################################################################
# CORE FUNCTION
###########################################################################

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

def execute_select(query, endpoint_url):
    # Initialize the SPARQL wrapper
    sparql_wrapper = SPARQLWrapper(endpoint_url)
    
    # Set the query and return format
    sparql_wrapper.setQuery(query)
    sparql_wrapper.setReturnFormat(JSON)
    
    # Execute the query and get the results
    results = sparql_wrapper.query().convert()
    
    # Process the results into a list of n-tuples
    bindings = results["results"]["bindings"]
    
    variables = results["head"]["vars"]  # Get the list of variable names
    q_variables = [f"?{v}" for v in variables]
    
    query_res = []
    
    for binding in bindings:
        # Create a tuple of values for each row
        row = tuple(binding[var]["value"] for var in variables if var in binding)
        query_res.append(row)
    
    triples = extract_triples(query)

    # Removing duplicated triples
    res_set = set()
    
    for t in triples: # (subj, pred, obj)
        if t[0] in q_variables and t[2] in q_variables:
            for row in query_res:
                res_set.add((row[q_variables.index(t[0])], t[1], row[q_variables.index(t[2])]))
        elif t[0] in q_variables and not t[2].startswith("?"):
            for row in query_res:
                res_set.add((row[q_variables.index(t[0])], t[1], t[2]))
        elif t[2] in q_variables and not t[0].startswith("?"):
            for row in query_res:
                res_set.add((t[0], t[1], row[q_variables.index(t[2])]))
    
    return list(res_set)

def extract_sparql_qwen(text: str) -> str:
    """
    Extracts the SPARQL query from a given text string.
    
    The function looks for the SPARQL query enclosed within triple backticks
    following the '<|im_start|>assistant' marker.
    
    Args:
        text (str): The input string containing the SPARQL query.
        
    Returns:
        str: The extracted SPARQL query. Returns an empty string if not found.
    """
    # Define a regex pattern to find the SPARQL query
    # It looks for <|im_start|>assistant followed by optional whitespace,
    # then triple backticks, captures everything non-greedily until the next triple backticks.
    pattern = r"<\|im_start\|>assistant\s*```\s*(.*?)\s*```"
    
    # Use re.DOTALL to ensure that the '.' character matches newline characters as well
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        sparql_query = match.group(1).strip()
        return sparql_query
    else:
        print("No SPARQL query found in the provided text.")
        return ""
    
def save_checkpoint(contexts, current_idx, name, checkpoint_file):
    """Save partial results to a checkpoint file."""
    checkpoint_data = {
        "contexts": contexts,
        "current_idx": current_idx
    }
    with open(checkpoint_file, 'wb') as f:
        pickle.dump(checkpoint_data, f)
    print(f"[Checkpoint Saved] {name}: Index {current_idx}")

def load_checkpoint(checkpoint_file):
    """Load checkpoint file if it exists."""
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'rb') as f:
            checkpoint_data = pickle.load(f)
        print(f"[Checkpoint Loaded] Resuming from Index {checkpoint_data['current_idx']}")
        return checkpoint_data["contexts"], checkpoint_data["current_idx"]
    print("[No Checkpoint Found] Starting from scratch.")
    return [], 0

def cleanup_checkpoints(checkpoint_dir, name):
    """Delete all checkpoint files associated with a name."""
    for filename in os.listdir(checkpoint_dir):
        if name in filename:
            os.remove(os.path.join(checkpoint_dir, filename))
            print(f"[Checkpoint Deleted] {filename}")