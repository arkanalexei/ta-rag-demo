from langchain_community.graphs import OntotextGraphDBGraph


class GraphDBStore:
    def __init__(self, config: dict):
        self.config = config
        self.graph = OntotextGraphDBGraph(query_endpoint=config["graphdb_uri"], local_file="./triple-uu/LexidOntologyUU_v4.ttl")

    def get_graph(self):
        return self.graph