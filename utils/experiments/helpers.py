import random
from itertools import zip_longest
from deep_translator import GoogleTranslator
from langdetect import detect
from transformers import XLMRobertaTokenizer

tokenizer = XLMRobertaTokenizer.from_pretrained("xlm-roberta-large")

def split_to_chunks(text, chunk_size, chunk_overlap):
    # split context into chunks based on chunk_size and chunk_overlap
    tokens = tokenizer.encode(text)
    num_tokens = len(tokens)

    # print(f"Total tokens: {num_tokens}")
    
    chunks = []
    for j in range(0, num_tokens, chunk_size - chunk_overlap):
        chunk_tokens = tokens[j:j + chunk_size]
        
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True, max_length=None)
        chunks.append(chunk_text)
        
        if j + chunk_size >= num_tokens:
            break

    return chunks

def random_except(n, x):
    # return a random number between 0 and n except x
    n -= 1
    result = random.randint(0, n)
    while result == x:
        result = random.randint(0, n)
    return result

def alternate_chunks(chunk_a, chunk_b):
    # a = [1,2]
    # b = [3,4]
    # result = [1,3,2,4]
    return [x for pair in zip_longest(chunk_a, chunk_b) for x in pair if x is not None]

translator_en = GoogleTranslator(source='auto', target='en')

def translate_to_eng(query):
    # if indonesian, translate to english
    # otherwise, return original
    try:
        lang = detect(query)
        if lang == "id":
            return translator_en.translate(query)
        return query
    except Exception as e:
        return query