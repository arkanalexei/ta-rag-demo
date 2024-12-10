from langchain_core.prompts import PromptTemplate
from tqdm import tqdm
from utils.database.qdrant import QdrantIndexManager
from utils.experiments.helpers import translate_to_eng
from utils.experiments.metrics import evaluate_all_metrics
from utils.llm import get_embedding_model, get_llm
from utils.prompt.main import QA_SYSTEM_PROMPT_UU_COT
from utils.retriever.uu.embedding_uu import get_embedding_uu
from utils.utils import load_from_pickle, save_to_pickle, set_gpu
from utils.config import get_config
from utils.retriever.uu.graph_uu import get_graph_from_custom_graphdb_uu, get_prompt_template
from utils.prompt.graph import *
from utils.utils import verbalize_triples
from utils.graph import execute_construct, execute_select, save_checkpoint, load_checkpoint, cleanup_checkpoints
from rdflib import Graph
import os
import pickle
import math

### DO NOT CHANGE BELOW THIS ###
gpu_no = int(input("Select GPU Number: "))
set_gpu(gpu_no)

def save_completed_scenarios():
    """Save the completed scenarios to a file."""
    with open(completed_scenarios_file, "wb") as f:
        pickle.dump(completed_scenarios, f)
    print("[Tracker Updated] Completed scenarios saved.")

# Define the completed scenarios tracker
completed_scenarios_file = "./pickles/completed_scenarios.pkl"

# Load completed scenarios
if os.path.exists(completed_scenarios_file):
    with open(completed_scenarios_file, "rb") as f:
        completed_scenarios = pickle.load(f)
    print(f"[Tracker Loaded] Completed scenarios: {completed_scenarios}")
else:
    completed_scenarios = []



# Define checkpoint directory
checkpoint_dir = "./checkpoints"
os.makedirs(checkpoint_dir, exist_ok=True)

shot_map = [
        # (1, "construct", False, "1_c_f"),
        # (2, "construct", False, "2_c_f"),
        # (3, "construct", False, "3_c_f"),
        # (4, "construct", False, "4_c_f"),
        # (5, "construct", False, "5_c_f"),
        
        # (1, "select", False, "1_s_f"),
        # (2, "select", False, "2_s_f"),
        # (3, "select", False, "3_s_f"),
        # (4, "select", False, "4_s_f"),
        # (5, "select", False, "5_s_f"),
        
        # (1, "construct", True, "1_c_t"),
        # (2, "construct", True, "2_c_t"),
        # (3, "construct", True, "3_c_t"),
        # (4, "construct", True, "4_c_t"),
        # (5, "construct", True, "5_c_t"),
        
        # (1, "select", True, "1_s_t"),
        # (2, "select", True, "2_s_t"),
        # (3, "select", True, "3_s_t"),
        # (4, "select", True, "4_s_t"),
        # (5, "select", True, "5_s_t"),

        # Canceled because the scenario taking too much time
        (0, "construct", False, "0_c_f"),
        (0, "select", False, "0_s_f"),
        (0, "construct", True, "0_c_t"),
        (0, "select", True, "0_s_t"),
]

llm = get_llm("nvidia-llama3.1")
config = get_config()
embed_model = get_embedding_model("BAAI/bge-m3")

# Turtle file location
turtle_file = "./triple-uu/LexidOntologyUU_v5.ttl"
# Load the Turtle file into an rdflib graph
g = Graph()
g.parse(turtle_file, format="turtle")
# Serialize the graph to a Turtle string
ontology_str = g.serialize(format="turtle")

testset = load_from_pickle('sampled_graph_dataset')
testset2 = testset

nrows = len(testset2)
questions = testset2["cleaned_question"].tolist()
ground_truths = testset2["ground_truth"].tolist()

counter = 0
for k, query_type, is_cot, name in shot_map:
    # Check if the scenario has already been completed
    if name in completed_scenarios:
        print(f"[Skipping] {name} already completed.")
        counter += 1
        continue

    print(f"[Processing] {name}")
    contexts = []
    template = get_prompt_template(k, query_type, is_cot)

    # Define checkpoint file
    checkpoint_file = os.path.join(checkpoint_dir, f"{name}_checkpoint.pkl")

    # Load checkpoint if available
    contexts, start_idx = load_checkpoint(checkpoint_file)
    # Setting up prompt template
    template = get_prompt_template(k, query_type, is_cot)
    # print(len(contexts[187]))
    # print(type(contexts[187]))
    
    #### GRAPH CONTEXT RETRIEVAL ####
    for i in tqdm(range(start_idx, nrows), initial=start_idx, desc=f"Generating {name} Graph context ({counter+1}/{len(shot_map)})"):
        
        # question
        question = questions[i]
    
        # prompt and SPARQL query generation
        prompt = PromptTemplate.from_template(template)
        prompt = prompt.format(prompt=question, schema=ontology_str)
    
        # llm and query extraction
        query = llm.invoke(prompt).content
        query_limit = f"{query} LIMIT 100"
    
        # query execution
        res_list = []
        try:
            if query_type == "construct":
                res_list = execute_construct(query=query_limit, endpoint_url=config["graphdb_uri"])
            elif query_type == "select":
                res_list = execute_select(query=query_limit, endpoint_url=config["graphdb_uri"])
        except Exception as e:
            print(f"[Error Executing Query: Question {i+1}]")
        # verbalize
        context = verbalize_triples(res_list)

        # context truncations
        context = context[:500] # Truncate to 500 elements

        # add to contexts
        contexts.append(context)

        # Save checkpoint every 5 rows
        if (i + 1) % 5 == 0 or (i + 1) == nrows:
            save_checkpoint(contexts, i + 1, name, checkpoint_file)
    
    #### BASELINE ####
    store = {}
    for i in tqdm(range(nrows), desc=f"Processing {name} Rows ({counter+1}/{len(shot_map)})"):
        # question
        question = questions[i]
    
        # ground truth
        ground_truth = translate_to_eng(ground_truths[i])
    
        # context, taken from the Graph Context Retrieval   
        bottom_context = contexts[i]

        # context truncations
        bottom_context = bottom_context[:500]  # Truncate to 500 elements
        if i == 3:
            print(bottom_context)
    
        # prompt
        prompt = PromptTemplate.from_template(QA_SYSTEM_PROMPT_UU_COT)
        prompt = prompt.format(context=bottom_context, question=question)
    
        # llm
        response = llm.invoke(prompt).content
    
        # evaluate
        results = evaluate_all_metrics(question, ground_truth, response, llm, embed_model)
    
        # put to dict
        store[i] = results

        # # Save checkpoint every 5 rows
        # if (i + 1) % 5 == 0 or (i + 1) == nrows:
        #     save_checkpoint(contexts, store, i + 1, name, checkpoint_file)
        
    save_to_pickle(store, name)
    print(f"[Final Save] {name}: Results saved.")

    # # Cleanup checkpoints
    # cleanup_checkpoints(checkpoint_dir, name)

    completed_scenarios.append(name)
    save_completed_scenarios()
    
    counter += 1

print("ALL DONE!!")
