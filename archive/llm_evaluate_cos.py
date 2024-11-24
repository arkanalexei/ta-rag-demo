from langchain_core.prompts import PromptTemplate
from tqdm import tqdm
from utils.database.qdrant import QdrantIndexManager
from utils.experiments.helpers import (alternate_chunks, random_except,
                                       split_to_chunks, translate_to_eng)
from utils.experiments.metrics import evaluate_all_metrics
from utils.llm import get_embedding_model, get_llm
from utils.prompt.main import QA_SYSTEM_PROMPT_UU_COT
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


# #### BOTTOM ####
# cos_512_128_bottom = {}

# for i in tqdm(range(nrows), desc="Processing Bottom Rows"):
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

#     bottom_context = chunks + noise_chunks

#     # prompt
#     prompt = PromptTemplate.from_template(QA_SYSTEM_PROMPT_UU_COT)
#     prompt = prompt.format(context=bottom_context, question=question)

#     # llm
#     response = llm.invoke(prompt).content

#     # evaluate
#     results = evaluate_all_metrics(question, ground_truth, response, llm, embed_model)

#     # put to dict
#     cos_512_128_bottom[i] = results

# save_to_pickle(cos_512_128_bottom, f'cos_{CHUNK_SIZE}_{CHUNK_OVERLAP}_bottom')

# #### ALTERNATE ####
# cos_512_128_alternate = {}

# for i in tqdm(range(nrows), desc="Processing Alternate Rows"):
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

#     bottom_context = alternate_chunks(chunks, noise_chunks)

#     # prompt
#     prompt = PromptTemplate.from_template(QA_SYSTEM_PROMPT_UU_COT)
#     prompt = prompt.format(context=bottom_context, question=question)

#     # llm
#     response = llm.invoke(prompt).content

#     # evaluate
#     results = evaluate_all_metrics(question, ground_truth, response, llm, embed_model)

#     # put to dict
#     cos_512_128_alternate[i] = results

# save_to_pickle(cos_512_128_alternate, f'cos_{CHUNK_SIZE}_{CHUNK_OVERLAP}_alternate')


# #### TOP ####
cos_512_128_top = {}

for i in tqdm(range(nrows), desc="Processing Top Rows"):
    # question
    question = questions[i]

    # ground truth
    ground_truth = translate_to_eng(ground_truths[i])

    # context
    random_i = random_except(nrows, i)

    context = contexts[i][0]
    noise_context = contexts[random_i][0]

    chunks = split_to_chunks(context, CHUNK_SIZE, CHUNK_OVERLAP)
    noise_chunks = split_to_chunks(noise_context, CHUNK_SIZE, CHUNK_OVERLAP)

    bottom_context = noise_chunks + chunks

    # prompt
    prompt = PromptTemplate.from_template(QA_SYSTEM_PROMPT_UU_COT)
    prompt = prompt.format(context=bottom_context, question=question)

    # llm
    response = llm.invoke(prompt).content

    # evaluate
    results = evaluate_all_metrics(question, ground_truth, response, llm, embed_model)

    # put to dict
    cos_512_128_top[i] = results

save_to_pickle(cos_512_128_top, f'cos_{CHUNK_SIZE}_{CHUNK_OVERLAP}_top')

#### NO CONTEXT ####
# cos_512_128_nocontext = {}

# for i in tqdm(range(nrows), desc="Processing No Context Rows"):
#     # question
#     question = questions[i]

#     # ground truth
#     ground_truth = translate_to_eng(ground_truths[i])

#     # context
#     bottom_context = []

#     # prompt
#     prompt = PromptTemplate.from_template(QA_SYSTEM_PROMPT_UU_COT)
#     prompt = prompt.format(context=bottom_context, question=question)

#     # llm
#     response = llm.invoke(prompt).content

#     # evaluate
#     results = evaluate_all_metrics(question, ground_truth, response, llm, embed_model)

#     # put to dict
#     cos_512_128_nocontext[i] = results

# save_to_pickle(cos_512_128_nocontext, f'cos_{CHUNK_SIZE}_{CHUNK_OVERLAP}_nocontext')

#### TOP 256 - 64 ####
CHUNK_SIZE = 256
CHUNK_OVERLAP = 64

cos_256_64_top = {}

for i in tqdm(range(nrows), desc="Processing 256 64 Top Rows"):
    # question
    question = questions[i]

    # ground truth
    ground_truth = translate_to_eng(ground_truths[i])

    # context
    random_i = random_except(nrows, i)

    context = contexts[i][0]
    noise_context = contexts[random_i][0]

    chunks = split_to_chunks(context, CHUNK_SIZE, CHUNK_OVERLAP)
    noise_chunks = split_to_chunks(noise_context, CHUNK_SIZE, CHUNK_OVERLAP)

    bottom_context = noise_chunks + chunks

    # prompt
    prompt = PromptTemplate.from_template(QA_SYSTEM_PROMPT_UU_COT)
    prompt = prompt.format(context=bottom_context, question=question)

    # llm
    response = llm.invoke(prompt).content

    # evaluate
    results = evaluate_all_metrics(question, ground_truth, response, llm, embed_model)

    # put to dict
    cos_256_64_top[i] = results

save_to_pickle(cos_256_64_top, f'cos_{CHUNK_SIZE}_{CHUNK_OVERLAP}_top')

#### TOP 1024 - 256 ####
CHUNK_SIZE = 1024
CHUNK_OVERLAP = 256

cos_1024_256_top = {}

for i in tqdm(range(nrows), desc="Processing 1024 256 Top Rows"):
    # question
    question = questions[i]

    # ground truth
    ground_truth = translate_to_eng(ground_truths[i])

    # context
    random_i = random_except(nrows, i)

    context = contexts[i][0]
    noise_context = contexts[random_i][0]

    chunks = split_to_chunks(context, CHUNK_SIZE, CHUNK_OVERLAP)
    noise_chunks = split_to_chunks(noise_context, CHUNK_SIZE, CHUNK_OVERLAP)

    bottom_context = noise_chunks + chunks

    # prompt
    prompt = PromptTemplate.from_template(QA_SYSTEM_PROMPT_UU_COT)
    prompt = prompt.format(context=bottom_context, question=question)

    # llm
    response = llm.invoke(prompt).content

    # evaluate
    results = evaluate_all_metrics(question, ground_truth, response, llm, embed_model)

    # put to dict
    cos_1024_256_top[i] = results

save_to_pickle(cos_1024_256_top, f'cos_{CHUNK_SIZE}_{CHUNK_OVERLAP}_top')