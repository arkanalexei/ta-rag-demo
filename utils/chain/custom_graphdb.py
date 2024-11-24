from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    import rdflib
    
from langchain.chains import OntotextGraphDBQAChain
from langchain_core.callbacks.manager import CallbackManager, CallbackManagerForChainRun

class CustomOntotextGraphDBQAChain(OntotextGraphDBQAChain):
    def __init__(self, **kwargs: Any) -> None:
        """Initialize the chain."""
        super().__init__(**kwargs)
            
    def _call(self, inputs: Dict[str, Any], run_manager=None):
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        callbacks = _run_manager.get_child()
        prompt = inputs[self.input_key]
        ontology_schema = self.graph.get_schema

        sparql_generation_chain_result = self.sparql_generation_chain.invoke(
            {"prompt": prompt, "schema": ontology_schema}, callbacks=callbacks
        )
        generated_sparql = sparql_generation_chain_result[
            self.sparql_generation_chain.output_key
        ]

        generated_sparql = self._get_prepared_sparql_query(
            _run_manager, callbacks, generated_sparql, ontology_schema
        )
        query_results = self._execute_query(generated_sparql)

        qa_chain_result = self.qa_chain.invoke(
            {"prompt": prompt, "context": query_results}, callbacks=callbacks
        )
        result = qa_chain_result[self.qa_chain.output_key]
        return {self.output_key: result, "generated_sparql": generated_sparql, "query_results": query_results}