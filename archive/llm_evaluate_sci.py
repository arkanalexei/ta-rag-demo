from langchain_core.prompts import PromptTemplate
from tqdm import tqdm
from utils.database.qdrant import QdrantIndexManager
from utils.experiments.helpers import (random_except,
                                       split_to_chunks, translate_to_eng)
from utils.experiments.metrics import evaluate_all_metrics
from utils.llm import get_embedding_model, get_llm
from utils.prompt.main import QA_SYSTEM_PROMPT_UU_COT
from utils.retriever.uu.embedding_uu import get_embedding_uu
from utils.utils import load_from_pickle, save_to_pickle, set_gpu
import random

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



# #### SINGLE NOISE ####
# fci_512_128_single = {}

# for i in tqdm(range(nrows), desc=f"Processing fci_{CHUNK_SIZE}_{CHUNK_OVERLAP}_single Rows"):
#     # question
#     question = questions[i]

#     # ground truth
#     ground_truth = translate_to_eng(ground_truths[i])

#     # context
#     random_i = random_except(nrows, i)

#     context = contexts[i][0]
#     noise_context = contexts[random_i][0]

#     chunks = split_to_chunks(context, CHUNK_SIZE, CHUNK_OVERLAP)
#     noise_chunks = split_to_chunks(noise_context, CHUNK_SIZE, CHUNK_OVERLAP)
#     noise_chunk = [random.choice(noise_chunks)]

#     bottom_context = chunks + noise_chunk
#     random.shuffle(bottom_context)

#     # prompt
#     prompt = PromptTemplate.from_template(QA_SYSTEM_PROMPT_UU_COT)
#     prompt = prompt.format(context=bottom_context, question=question)

#     # llm
#     response = llm.invoke(prompt).content

#     # evaluate
#     results = evaluate_all_metrics(question, ground_truth, response, llm, embed_model)

#     # put to dict
#     fci_512_128_single[i] = results

# save_to_pickle(fci_512_128_single, 'fci_512_128_single')

# #### MULTIPLE NOISE ####
# fci_512_128_multiple = {}

# for i in tqdm(range(nrows), desc=f"Processing fci_{CHUNK_SIZE}_{CHUNK_OVERLAP}_multiple Rows"):
#     # question
#     question = questions[i]

#     # ground truth
#     ground_truth = translate_to_eng(ground_truths[i])

#     # context
#     random_i = random_except(nrows, i)

#     context = contexts[i][0]
#     noise_context = contexts[random_i][0]

#     chunks = split_to_chunks(context, CHUNK_SIZE, CHUNK_OVERLAP)
#     noise_chunks = split_to_chunks(noise_context, CHUNK_SIZE, CHUNK_OVERLAP)
#     num_noise = random.randint(1, len(noise_chunks))
#     random_noise_chunks = random.sample(noise_chunks, num_noise)

#     bottom_context = chunks + random_noise_chunks
#     random.shuffle(bottom_context)

#     # prompt
#     prompt = PromptTemplate.from_template(QA_SYSTEM_PROMPT_UU_COT)
#     prompt = prompt.format(context=bottom_context, question=question)

#     # llm
#     response = llm.invoke(prompt).content

#     # evaluate
#     results = evaluate_all_metrics(question, ground_truth, response, llm, embed_model)

#     # put to dict
#     fci_512_128_multiple[i] = results

# save_to_pickle(fci_512_128_multiple, 'fci_512_128_multiple')

# #### NO NOISE ####
# fci_512_128_nonoise = {}

# for i in tqdm(range(nrows), desc=f"Processing fci_{CHUNK_SIZE}_{CHUNK_OVERLAP}_nonoise Rows"):
#     # question
#     question = questions[i]

#     # ground truth
#     ground_truth = translate_to_eng(ground_truths[i])

#     # context
#     context = contexts[i][0]

#     chunks = split_to_chunks(context, CHUNK_SIZE, CHUNK_OVERLAP)
#     bottom_context = chunks
#     random.shuffle(bottom_context)

#     # prompt
#     prompt = PromptTemplate.from_template(QA_SYSTEM_PROMPT_UU_COT)
#     prompt = prompt.format(context=bottom_context, question=question)

#     # llm
#     response = llm.invoke(prompt).content

#     # evaluate
#     results = evaluate_all_metrics(question, ground_truth, response, llm, embed_model)

#     # put to dict
#     fci_512_128_nonoise[i] = results

# save_to_pickle(fci_512_128_nonoise, 'fci_512_128_nonoise')

#### NO NOISE - 256 64 ####
CHUNK_SIZE = 256
CHUNK_OVERLAP = 64

sci_256_64_nonoise = {}

for i in tqdm(range(nrows), desc=f"Processing sci_{CHUNK_SIZE}_{CHUNK_OVERLAP}_nonoise Rows"):
    # question
    question = questions[i]

    # ground truth
    ground_truth = translate_to_eng(ground_truths[i])

    # context
    context = contexts[i][0]

    chunks = split_to_chunks(context, CHUNK_SIZE, CHUNK_OVERLAP)
    bottom_context = chunks
    random.shuffle(bottom_context)

    # prompt
    prompt = PromptTemplate.from_template(QA_SYSTEM_PROMPT_UU_COT)
    prompt = prompt.format(context=bottom_context, question=question)

    # llm
    response = llm.invoke(prompt).content

    # evaluate
    results = evaluate_all_metrics(question, ground_truth, response, llm, embed_model)

    # put to dict
    sci_256_64_nonoise[i] = results

save_to_pickle(sci_256_64_nonoise, 'sci_256_64_nonoise')

#### NO NOISE - 1024 256 ####
CHUNK_SIZE = 1024
CHUNK_OVERLAP = 256

sci_1024_256_nonoise = {}

for i in tqdm(range(nrows), desc=f"Processing sci_{CHUNK_SIZE}_{CHUNK_OVERLAP}_nonoise Rows"):
    # question
    question = questions[i]

    # ground truth
    ground_truth = translate_to_eng(ground_truths[i])

    # context
    context = contexts[i][0]

    chunks = split_to_chunks(context, CHUNK_SIZE, CHUNK_OVERLAP)
    bottom_context = chunks
    random.shuffle(bottom_context)

    # prompt
    prompt = PromptTemplate.from_template(QA_SYSTEM_PROMPT_UU_COT)
    prompt = prompt.format(context=bottom_context, question=question)

    # llm
    response = llm.invoke(prompt).content

    # evaluate
    results = evaluate_all_metrics(question, ground_truth, response, llm, embed_model)

    # put to dict
    sci_1024_256_nonoise[i] = results

save_to_pickle(sci_1024_256_nonoise, 'sci_1024_256_nonoise')
