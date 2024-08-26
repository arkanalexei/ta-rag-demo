from typing import Sequence, Union

from langchain.chains.query_constructor.base import (
    AttributeInfo, StructuredQueryOutputParser, get_query_constructor_prompt)
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_community.document_transformers.embeddings_redundant_filter import \
    _DocumentWithState
from langchain_community.query_constructors.qdrant import QdrantTranslator
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.prompts import BasePromptTemplate, PromptTemplate
from langchain_core.vectorstores import VectorStore

DEFAULT_SCHEMA = """\
<< Structured Request Schema >>
When responding use a markdown code snippet with a JSON object formatted in the following schema:

```json
{{{{
    "query": string \\ text string to compare to document contents
    "filter": string \\ logical condition statement for filtering documents
}}}}
```

The query string should contain only text that is expected to match the contents of documents. Any conditions in the filter should not be mentioned in the query as well.

A logical condition statement is composed of one or more comparison and logical operation statements.

A comparison statement takes the form: `comp(attr, val)`:
- `comp` ({allowed_comparators}): comparator
- `attr` (string):  name of attribute to apply the comparison to
- `val` (string): is the comparison value

A logical operation statement takes the form `op(statement1, statement2, ...)`:
- `op` ({allowed_operators}): logical operator
- `statement1`, `statement2`, ... (comparison statements or logical operation statements): one or more statements to apply the operation to

Make sure that you only use the comparators and logical operators listed above and no others.
Make sure that filters only refer to attributes that exist in the data source.
Make sure that filters only use the attributed names with its function names if there are functions applied on them.
Make sure that filters only use format `YYYY/MM/DD` when handling date data typed values.
Make sure that filters take into account the descriptions of attributes and only make comparisons that are feasible given the type of data being stored.
Make sure that filters are only used as needed. If there are no filters that should be applied return "NO_FILTER" for the filter value.\
"""

DEFAULT_SCHEMA_PROMPT = PromptTemplate.from_template(DEFAULT_SCHEMA)

def to_documents(context: list[_DocumentWithState]):
    context_unique = [i.to_document() for i in context]
    return context_unique

def self_query(llm_model: BaseLanguageModel, vector_store: VectorStore, document_content_description: str, metadata_field_info: Sequence[Union[AttributeInfo, dict]], search_type: str = "similarity", schema_prompt: BasePromptTemplate = DEFAULT_SCHEMA_PROMPT, top_k: int = 8) -> SelfQueryRetriever:
    translator = QdrantTranslator(metadata_key="metadata")
    prompt = get_query_constructor_prompt(
        document_contents=document_content_description,
        attribute_info=metadata_field_info,
        schema_prompt=schema_prompt,
        allowed_comparators=translator.allowed_comparators,
        allowed_operators=translator.allowed_operators
    )

    output_parser = StructuredQueryOutputParser.from_components()
    query_constructor = prompt | llm_model | output_parser

    retriever = SelfQueryRetriever(
        query_constructor=query_constructor,
        vectorstore=vector_store,
        search_type=search_type,
        search_kwargs={'k': top_k}
    )

    if search_type == "mmr":
        retriever = SelfQueryRetriever(
        query_constructor=query_constructor,
        vectorstore=vector_store,
        search_type=search_type,
        search_kwargs={'k': top_k, 'lambda_mult': 0.85, 'fetch_k': 40}
    )

    return retriever