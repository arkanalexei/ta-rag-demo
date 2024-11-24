from langchain_core.prompts import PromptTemplate
from tqdm import tqdm
from utils.database.qdrant import QdrantIndexManager
from utils.experiments.helpers import translate_to_eng, split_to_chunks
from utils.experiments.metrics import evaluate_all_metrics
from utils.llm import get_embedding_model, get_llm
from utils.prompt.main import QA_SYSTEM_PROMPT_UU_COT, QA_SYSTEM_PROMPT_UU_ZEROSHOT, QA_SYSTEM_PROMPT_UU_FEWSHOT
from utils.retriever.uu.embedding_uu import get_embedding_uu
from utils.utils import load_from_pickle, save_to_pickle, set_gpu

CHUNK_SIZE = 512
CHUNK_OVERLAP = 128

### DO NOT CHANGE BELOW THIS ###
set_gpu(5)

llm = get_llm("nvidia-llama3.1")
embed_model = get_embedding_model("BAAI/bge-m3")

vector_store = QdrantIndexManager(embed_model=embed_model, index_name="uu-all").load_vector_index()
retriever_uu = get_embedding_uu(vector_store=vector_store, llm=llm, embed_model=embed_model)

testset = load_from_pickle('validated_testset')
testset2 = testset

nrows = len(testset2)
questions = testset2["cleaned_question"].tolist()
contexts = testset2["contexts"].tolist()
ground_truths = testset2["ground_truth"].tolist()


#### Zero Shot ####
sp_zero = {}

for i in tqdm(range(nrows), desc=f"Processing zero shot Rows"):
    # question
    question = questions[i]

    # ground truth
    ground_truth = translate_to_eng(ground_truths[i])

    # context
    context = contexts[i][0]
    
    chunks = split_to_chunks(context, CHUNK_SIZE, CHUNK_OVERLAP)
    bottom_context = chunks

    # prompt
    prompt = PromptTemplate.from_template(QA_SYSTEM_PROMPT_UU_ZEROSHOT)
    prompt = prompt.format(context=bottom_context, question=question)

    # llm
    response = llm.invoke(prompt).content

    # evaluate
    results = evaluate_all_metrics(question, ground_truth, response, llm, embed_model)

    # put to dict
    sp_zero[i] = results

save_to_pickle(sp_zero, 'sp_zero')

#### Few Shot ####
sp_few = {}

for i in tqdm(range(nrows), desc=f"Processing few shot Rows"):
    # question
    question = questions[i]

    # ground truth
    ground_truth = translate_to_eng(ground_truths[i])

    # context
    context = contexts[i][0]
    
    chunks = split_to_chunks(context, CHUNK_SIZE, CHUNK_OVERLAP)
    bottom_context = chunks

    # prompt
    prompt = PromptTemplate.from_template(QA_SYSTEM_PROMPT_UU_FEWSHOT)
    prompt = prompt.format(context=bottom_context, question=question)

    # llm
    response = llm.invoke(prompt).content

    # evaluate
    results = evaluate_all_metrics(question, ground_truth, response, llm, embed_model)

    # put to dict
    sp_few[i] = results

save_to_pickle(sp_few, 'sp_few')

#### Chain of Thought ####
sp_cot = {}

for i in tqdm(range(nrows), desc=f"Processing CoT Rows"):
    # question
    question = questions[i]

    # ground truth
    ground_truth = translate_to_eng(ground_truths[i])

    # context
    context = contexts[i][0]
    
    chunks = split_to_chunks(context, CHUNK_SIZE, CHUNK_OVERLAP)
    bottom_context = chunks

    # prompt
    prompt = PromptTemplate.from_template(QA_SYSTEM_PROMPT_UU_COT)
    prompt = prompt.format(context=bottom_context, question=question)

    # llm
    response = llm.invoke(prompt).content

    # evaluate
    results = evaluate_all_metrics(question, ground_truth, response, llm, embed_model)

    # put to dict
    sp_cot[i] = results

save_to_pickle(sp_cot, 'sp_cot')