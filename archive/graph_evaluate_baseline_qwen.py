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
from utils.retriever.uu.graph_uu import get_graph_from_custom_graphdb_uu
from utils.graph import extract_sparql_qwen

### DO NOT CHANGE BELOW THIS ###
gpu_no = int(input("Select GPU Number: "))
set_gpu(gpu_no)

# k = int(input("Choose k-shot (0-5): "))
# query_type = input("Choose query type (select|construct): ")

# is_cot = input("Use CoT (y/n): ")
# if is_cot = "y":
#     is_cot = True
# elif is_cot = "n":
#     is_cot = False

llm = get_llm("hf-qwen-coder2.5")
config = get_config()
embed_model = get_embedding_model("BAAI/bge-m3")

retriever_uu = get_graph_from_custom_graphdb_uu(llm=llm, config=config)

testset = load_from_pickle('sampled_graph_dataset')
testset2 = testset

nrows = len(testset2)
questions = testset2["cleaned_question"].tolist()
contexts = ["" for _ in questions]
ground_truths = testset2["ground_truth"].tolist()

# #### GRAPH CONTEXT GENERATION ####
# for i in tqdm(range(nrows), desc=f"Generated baseline SPARQL"):
#     # question
#     question = questions[i]

#     # prompt
    

#     # llm
#     response = llm.invoke(prompt).content

#     # evaluate
#     results = evaluate_all_metrics(question, ground_truth, response, llm, embed_model)

#     # put to dict
#     baseline[i] = results


#### BASELINE ####
baseline = {}

for i in tqdm(range(nrows), desc=f"Processing baseline Rows"):
    # question
    question = questions[i]

    # ground truth
    ground_truth = translate_to_eng(ground_truths[i])

    # context, empty because it's baseline
    context = ""

    bottom_context = [context]

    # prompt
    prompt = PromptTemplate.from_template(QA_SYSTEM_PROMPT_UU_COT)
    prompt = prompt.format(context=bottom_context, question=question)

    # llm
    response = llm.invoke(prompt).content

    # evaluate
    results = evaluate_all_metrics(question, ground_truth, response, llm, embed_model)

    # put to dict
    baseline[i] = results
    
save_to_pickle(baseline, 'baseline_ttl')

print("Baseline evaluation DONE!")
