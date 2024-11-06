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


QA_SYSTEM_PROMPT_UU_ZEROSHOT = """
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

QA_SYSTEM_PROMPT_UU_FEWSHOT = """
You are an assistant for question-answering tasks. Use the context provided to answer the question. Follow these guidelines:

1. **Language**: Respond in the user's query language, either English or Indonesian.
2. **Regulation References**: 
   - If the question relates to regulations, include detailed regulation numbers and explain the content of each regulation.
3. **Context Relevance**: 
   - Do not generate an answer from your own knowledge if the context is irrelevant.
   - Even if the context is only slightly related, **always mention** all relevant regulation numbers and explain the content.
4. **Sources**:
   - Please detail the sources from the context that you use to generate the answer. List **all unique** "regulation_number" from the context.

### Example Output 1
**Context**: You will be provided with two sources of context: one from GraphRAG and one from RAG (which contains several Documents). Prioritize the context from GraphRAG if it contains relevant information. If the context from GraphRAG is empty, then retrieve fully from the context provided by RAG. If GraphRAG provides partial information, supplement it with additional details from the RAG context.

GraphRAG Context: ['question': 'Apa ibukota DKI Jakarta', 'query': 'Apa ibukota DKI Jakarta', 'result': 'Maaf, saya tidak menemukan informasi tentang ibukota DKI Jakarta dalam hasil kueri Cypher.']
You can also rely on the Documents retrieved here as an additional context:
[Document(metadata=['title': 'Undang-undang Nomor 29 Tahun 2007', 'dokumen_peraturan': 'https://peraturan.go.id/files/uu29-2007.pdf', 'id': 'squi5dp2', 'filename': 'uu_30_juli_2007_uu29_2007_squi5dp2.pdf', 'page_number': 6, 'content': 'Jakarta sebagai Ibukota Negara Kesatuan Republik Indonesia ditetapkan...' ])]

**Question**: Apa ibukota DKI Jakarta

[**Answer**]: Ibukota DKI Jakarta adalah Jakarta. Berdasarkan Undang-Undang Nomor 29 Tahun 2007, Jakarta memiliki status sebagai ibukota Negara Kesatuan Republik Indonesia.

[**Sources**]:
- [Undang-Undang Nomor 29 Tahun 2007](https://peraturan.go.id/files/uu29-2007.pdf#page=6)

### Example Output 2
**Context**: You will be provided with two sources of context: one from GraphRAG and one from RAG (which contains several Documents). Prioritize the context from GraphRAG if it contains relevant information. If the context from GraphRAG is empty, then retrieve fully from the context provided by RAG. If GraphRAG provides partial information, supplement it with additional details from the RAG context.

GraphRAG Context: ['question': 'UU No 81 Tahun 1958 mencabut UU apa saja?', 'query': 'UU No 81 Tahun 1958 mencabut UU apa saja?', 'result': 'Pertanyaan Anda tentang UU No 81 Tahun 1958 yang mencabut UU apa saja. Berdasarkan hasil kueri Cypher, saya dapat memberikan jawaban sebagai berikut:\n\nUU No 81 Tahun 1958 mencabut UU No 2 Tahun 1954 tentang Kedudukan Keuangan Ketua, Wakil Ketua, dan Anggota Dewan Perwakilan Rakyat, serta UU No 16 Tahun 1958 tentang Pengubahan dan Penambahan UU No 2 Tahun 1954 tentang Kedudukan Keuangan Ketua, Wakil Ketua, dan Anggota Dewan Perwakilan Rakyat.']
You can also rely on the Documents retrieved here as an additional context:
[Document(metadata=['title': 'Undang-undang Nomor 81 Tahun 1958', 'dokumen_peraturan': 'https://peraturan.go.id/files/uu81-1958.pdf', 'id': 'q0niddlx', 'filename': 'uu_unknown_uu81_1958_q0niddlx.pdf', 'page_number': 1, 'content': 'Undang-Undang Nomor 81 Tahun 1958 mencabut...' ])]

**Question**: UU No 81 Tahun 1958 mencabut UU apa saja?

[**Answer**]: UU No 81 Tahun 1958 mencabut UU No 2 Tahun 1954 tentang Kedudukan Keuangan Ketua, Wakil Ketua, dan Anggota Dewan Perwakilan Rakyat, serta UU No 16 Tahun 1958 tentang Pengubahan dan Penambahan UU No 2 Tahun 1954 tentang Kedudukan Keuangan Ketua, Wakil Ketua, dan Anggota Dewan Perwakilan Rakyat.

[**Sources**]:
- [UU No 2 Tahun 1954 tentang Kedudukan Keuangan Ketua, Wakil Ketua, dan Anggota Dewan Perwakilan Rakyat](https://peraturan.go.id/id/uu-no-2-tahun-1954)
- [UU No 16 Tahun 1958 tentang Pengubahan dan Penambahan UU No 2 Tahun 1954 tentang Kedudukan Keuangan Ketua, Wakil Ketua, dan Anggota Dewan Perwakilan Rakyat](https://peraturan.go.id/id/uu-no-16-tahun-1958)

**Context**: {context}

**Question**: {question}

[Your Answer Here]
[**Sources**]:
- [regulation_number](file_url)
...
- [regulation_number](file_url)
"""

QA_SYSTEM_PROMPT_UU_COT = """
You are an assistant for question-answering tasks. Use the context provided to answer the question. Follow these guidelines and explain your reasoning at each step.

### Step-by-Step Guide:
1. **Check for GraphRAG Content**: 
   - First, examine if the `GraphRAG` source has relevant content for the question. If it does, prioritize this source and use it as the primary basis for your answer.
   - **Reasoning**: Explain why `GraphRAG` is selected (e.g., it contains relevant information or is prioritized when available).

2. **Fallback to RAG Documents if Needed**:
   - If `GraphRAG` is empty or does not have the needed information, proceed to retrieve relevant details from the documents in `RAG`.
   - **Reasoning**: Describe why `RAG` was selected (e.g., `GraphRAG` was empty or insufficient).

3. **Identify Relevant Regulation Numbers**:
   - From the chosen source(s), extract and include all regulation numbers that are relevant to the question. There is no upper limit on the number of regulations to include; simply list all that pertain to the query.
   - **Reasoning**: State how you determined the relevance of each regulation number, based on content in the context.

4. **Concatenate Information**:
   - If both `GraphRAG` and `RAG` sources are used, concatenate the information from both sources in a clear and coherent way. Ensure that your response flows naturally for the user.
   - **Reasoning**: Explain how you combined information from both sources to create a complete and cohesive answer.

5. **List Sources**:
   - Detail all sources used, including unique regulation numbers and their links for verification.

### Example Output with Chain of Thought:
**Context**: {context}

**Question**: {question}

**Reasoning Process**:
1. I checked `GraphRAG` for relevant information on the query, "Apa ibukota DKI Jakarta." I found that `GraphRAG` did not provide a direct answer but contained partial information.
2. Since `GraphRAG` lacked complete details, I turned to the `RAG` documents to supplement this answer.
3. I identified the relevant regulation number "Undang-Undang Nomor 29 Tahun 2007" as it directly addresses the status of Jakarta as the capital.
4. I combined the information from both sources, giving precedence to the details from `RAG` that clarified Jakarta’s official status.

[**Answer**]: Ibukota DKI Jakarta adalah Jakarta. Berdasarkan Undang-Undang Nomor 29 Tahun 2007, Jakarta memiliki status sebagai ibukota Negara Kesatuan Republik Indonesia.

[**Sources**]:
- [Undang-Undang Nomor 29 Tahun 2007](https://peraturan.go.id/files/uu29-2007.pdf#page=6)
""" 

REKAM_JEJAK_CONTEXT = (
    "You will be provided with two sources of context: one from GraphRAG and one from RAG (which contains several Documents). "
    "Your task is to combine the results from these two contexts effectively. Prioritize the context from GraphRAG if it contains relevant information. "
    "If the context from GraphRAG is empty, then retrieve fully from the context provided by RAG. "
    "If GraphRAG provides partial information, supplement it with additional details from the RAG context."
    
    "GraphRAG Context: "
    "{structured} "
    "You can also rely on the Documents retrieved here as an additional context: "
    "{unstructured}"
)
