from langchain_core.prompts import PromptTemplate
from tqdm import tqdm
from utils.database.qdrant import QdrantIndexManager
from utils.experiments.helpers import translate_to_eng, split_to_chunks, alternate_chunks, random_except
from utils.experiments.metrics import evaluate_all_metrics
from utils.llm import get_embedding_model, get_llm
from utils.prompt.main import QA_SYSTEM_PROMPT_UU_COT
from utils.retriever.uu.embedding_uu import get_embedding_uu
from utils.utils import load_from_pickle, save_to_pickle, set_gpu
import random

### HELPER FUNCTIONS ###

def no_context(chunks, noise_chunks):
    return []

def no_noise(chunks, noise_chunks):
    return chunks

def bottom_single(chunks, noise_chunks):
    noise_chunk = [random.choice(noise_chunks)]
    return chunks + noise_chunk

def bottom_multiple(chunks, noise_chunks):
    num_noise = random.randint(1, len(noise_chunks))
    random_noise_chunks = random.sample(noise_chunks, num_noise)
    return chunks + random_noise_chunks

def alternate_single(chunks, noise_chunks):
    noise_chunk = [random.choice(noise_chunks)]
    return alternate_chunks(chunks, noise_chunk)

def alternate_multiple(chunks, noise_chunks):
    num_noise = random.randint(1, len(noise_chunks))
    random_noise_chunks = random.sample(noise_chunks, num_noise)
    return alternate_chunks(chunks, random_noise_chunks)

def top_single(chunks, noise_chunks):
    noise_chunk = [random.choice(noise_chunks)]
    return noise_chunk + chunks

def top_multiple(chunks, noise_chunks):
    num_noise = random.randint(1, len(noise_chunks))
    random_noise_chunks = random.sample(noise_chunks, num_noise)
    return random_noise_chunks + chunks

### END OF HELPER FUNCTIONS ###

CHUNK_SIZE = 512
CHUNK_OVERLAP = 128

# Strategies
strategies = {
    "No Context": no_context,
    "No Noise": no_noise,
    "Bottom Single": bottom_single,
    "Bottom Multiple": bottom_multiple,
    "Alternate Single": alternate_single,
    "Alternate Multiple": alternate_multiple,
    "Top Single": top_single,
    "Top Multiple": top_multiple
}

# Combinations
combinations = [
    ("Bottom Multiple", "cs_bm"),
]

# Generate the dictionary
config = {}
for i, (strategy, name) in enumerate(combinations):
    config[i] = {
        'strategy': strategies[strategy],
        'name': name
    }


### DO NOT CHANGE BELOW THIS ###
set_gpu(3)

llm = get_llm("nvidia-llama3.1", temperature=0.1, top_p=0.1)
embed_model = get_embedding_model("BAAI/bge-m3")

vector_store = QdrantIndexManager(embed_model=embed_model, index_name="uu-all").load_vector_index()
retriever_uu = get_embedding_uu(vector_store=vector_store, llm=llm, embed_model=embed_model)

testset = load_from_pickle('validated_testset')
testset2 = testset

nrows = len(testset2)
questions = testset2["cleaned_question"].tolist()
contexts = testset2["contexts"].tolist()
ground_truths = testset2["ground_truth"].tolist()


#### Trying out all combinations! ####
for k, v in config.items():
    strategy = v['strategy']
    name = v['name']

    store = {}

    for i in tqdm(range(nrows), desc=f"Processing {name} Rows ({k+1}/{len(config)})"):
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
        
        bottom_context = strategy(chunks, noise_chunks)
         
        # prompt
        prompt = PromptTemplate.from_template(QA_SYSTEM_PROMPT_UU_COT)
        prompt = prompt.format(context=bottom_context, question=question)
    
        # llm
        response = llm.invoke(prompt).content
    
        # evaluate
        results = evaluate_all_metrics(question, ground_truth, response, llm, embed_model)
    
        # put to dict
        store[i] = results

    save_to_pickle(store, name)

    
print("ALL DONE!!!")
