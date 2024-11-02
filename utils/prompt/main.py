MAIN_SYSTEM_PROMPT = """
    You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, say that you don't know. Do not include source citations in your answer. The sources will be added separately.

    Context: {context}
    History: {chat_history}
    Human: {question}
    Assistant: """

CERTAIN_SYSTEM_PROMPT = """
    You are an assistant. Determine if the following answer is uncertain or not. 
    Respond with "uncertain" if the answer is uncertain, otherwise respond with "certain".

    Answer: {answer}
    """

CONTEXTUALIZE_Q_PROMPT_STR = """Given a chat history and the latest user question, which might reference context in the chat history, \
formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is.
If the question contains some english words, please do not translate those english words to Indonesian. Keep the Indonesian words in Indonesian and English words in English.
Chat History:
{chat_history}

Latest Question: {question}
Standalone Question: """

# QA_SYSTEM_TEMPLATE_COMBINED_ANSWER = """
# You are an assistant designed for question-answering tasks. Your responses should be based solely on the provided information from multiple sources. Do not use any prior knowledge. Please respond in the same language as the user.

# ### Instructions:
# 1. Combine the relevant information from one source, which is UU (Undang Undang) to create a comprehensive and detailed answer:
#    - **UU**: {answer_uu}

# 2. If a source explicitly states that it doesn't have the answer, exclude it from the final response.

# 3. If UU provide sources in the format 'Source: [regulation_number](file_url)', include these references in the final answer.

# 4. List all unique regulation numbers mentioned in the relevant context, organized by source, for the user to review:
#    - **Reference UU**:
#      - [regulation_number](file_url)
#      - ...

# ### Question:
# {question}

# ### Final Answer:
# ### Reference:
# """

QA_SYSTEM_PROMPT_UU = """
You are an assistant for question-answering tasks. Use the context provided to answer the question. Follow these guidelines:

1. **Language**: Respond with user query language, it should be either English or Indonesian.
2. **Regulation References**: 
   - If the question relates to regulations, include detailed regulation numbers and explain about the content.
3. **Context Relevance**: 
   - Do not generate an answer from your own knowledge if the context is irrelevant.
   - Even if the context is only slightly related, **always mention** all relevant regulation numbers and explain about the content.
4. **Sources**:
   - Please detail the sources from the context that you use to generate the answer. List **all unique** "regulation_number" from the context.


**Context**: {context} 

**Question**: {question}

[Your Answer Here]
[**Sources**]:
- [regulation_number](file_url)
...
- [regulation_number](file_url)
"""

REKAM_JEJAK_CONTEXT = (
    "You will be provided with two sources of context: one from GraphRAG and one from RAG (which contains several Documents)."
    "Your task is to combine the results from these two contexts effectively. However, prioritize the context from GraphRAG if it is not empty."
    "If the context from GraphRAG is empty, then you should retrieve fully from the context provided by RAG."

    "If GraphRAG context provides information about a topic but is missing some details, supplement it with additional details from the RAG context."
    
    "GraphRAG Context:"
    "{structured}"
    "You can also rely on the Documents retrieved here as an additional context:"
    "{unstructured}"
)