from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.meteor_score import meteor_score
from rouge_score import rouge_scorer
from bert_score import score
from datasets import Dataset 
from ragas.metrics import answer_correctness, answer_similarity
from ragas import evaluate


# Assuming `a` is ground truth and `b` is the LLM output

def bleu(a, b):
    smooth_fn = SmoothingFunction().method1
    return sentence_bleu([a.split()], b.split(), smoothing_function=smooth_fn)

def rouge(a, b):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    return scorer.score(a, b)

def meteor(a, b):
    return meteor_score([a.split()], b.split())
    
def bert_score(a, b):
    P, R, F1 = score([b], [a], lang="en")
    return P, R, F1

def ragas(q, a, b):
    data_samples = {
        'question': [q],
        'answer': [b],
        'ground_truth': [a]
    }
    dataset = Dataset.from_dict(data_samples)
    score = evaluate(dataset, metrics=[answer_correctness, answer_similarity], llm=llm, embeddings=embed_model)
    return score

def evaluate_all_metrics(q, a, b, llm, embed_model):
    results = {}

    # General
    results['question'] = q
    results['ground_truth'] = a
    results['output'] = b

    # BLEU Score
    results['BLEU'] = bleu(a, b)
    
    # ROUGE Scores - capture precision, recall, and fmeasure for ROUGE-1, ROUGE-2, and ROUGE-L
    rouge_scores = rouge(a, b)
    results['ROUGE-1_Precision'] = rouge_scores['rouge1'].precision
    results['ROUGE-1_Recall'] = rouge_scores['rouge1'].recall
    results['ROUGE-1_F1'] = rouge_scores['rouge1'].fmeasure
    results['ROUGE-2_Precision'] = rouge_scores['rouge2'].precision
    results['ROUGE-2_Recall'] = rouge_scores['rouge2'].recall
    results['ROUGE-2_F1'] = rouge_scores['rouge2'].fmeasure
    results['ROUGE-L_Precision'] = rouge_scores['rougeL'].precision
    results['ROUGE-L_Recall'] = rouge_scores['rougeL'].recall
    results['ROUGE-L_F1'] = rouge_scores['rougeL'].fmeasure
    
    # METEOR Score
    results['METEOR'] = meteor(a, b)
    
    # BERTScore - capture individual precision, recall, and F1 scores
    P, R, F1 = bert_score(a, b)
    results['BERTScore_Precision'] = P.mean().item()  # Average over tokens
    results['BERTScore_Recall'] = R.mean().item()
    results['BERTScore_F1'] = F1.mean().item()

    # RAGAS metrics
    data_samples = {
        'question': [q],
        'answer': [b],
        'ground_truth': [a]
    }
    dataset = Dataset.from_dict(data_samples)
    # decided to omit answer_correctness
    ragas_scores = evaluate(dataset, metrics=[answer_similarity], llm=llm, embeddings=embed_model)
    
    # results['RAGAS_Answer_Correctness'] = ragas_scores['answer_correctness']
    results['RAGAS_Answer_Similarity'] = ragas_scores['answer_similarity']

    return results