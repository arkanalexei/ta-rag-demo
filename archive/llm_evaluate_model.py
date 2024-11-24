from langchain_core.prompts import PromptTemplate
from tqdm import tqdm
from utils.database.qdrant import QdrantIndexManager
from utils.experiments.helpers import translate_to_eng, split_to_chunks
from utils.experiments.metrics import evaluate_all_metrics
from utils.llm import get_embedding_model, get_llm
from utils.prompt.main import QA_SYSTEM_PROMPT_UU_COT
from utils.retriever.uu.embedding_uu import get_embedding_uu
from utils.utils import load_from_pickle, save_to_pickle, set_gpu
import torch
from transformers import pipeline

CHUNK_SIZE = 512
CHUNK_OVERLAP = 128

### DO NOT CHANGE BELOW THIS ###
set_gpu(5)

llm = get_llm("nvidia-llama3.1")
embed_model = get_embedding_model("BAAI/bge-m3")

testset = load_from_pickle('validated_testset')
testset2 = testset

nrows = len(testset2)
questions = testset2["cleaned_question"].tolist()
contexts = testset2["contexts"].tolist()
ground_truths = testset2["ground_truth"].tolist()

#### LLAMA 3.2 3B ####
model_id = "meta-llama/Llama-3.2-3B-Instruct"
pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map="sequential",
)

llmmodel_llama3b = {}

for i in tqdm(range(nrows), desc=f"Processing llmmodel_llama3b Rows"):
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
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": question},
    ]

    set_gpu(5)
    outputs = pipe(
        messages,
        max_new_tokens=16000,
        temperature=0.5,
        top_p=0.5
    )
    response = outputs[0]["generated_text"][-1]['content']

    # evaluate
    results = evaluate_all_metrics(question, ground_truth, response, llm, embed_model)

    # put to dict
    llmmodel_llama3b[i] = results

save_to_pickle(llmmodel_llama3b, 'llmmodel_llama3b')