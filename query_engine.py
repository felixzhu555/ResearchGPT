from llama_index import (
    ResponseSynthesizer,
    StorageContext,
    load_index_from_storage,
)
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.indices.postprocessor import SimilarityPostprocessor


# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="/Users/felix_3gpdyfd/ai hackathon/persist_index")

# load index
index = load_index_from_storage(storage_context)

# configure retriever
retriever = VectorIndexRetriever(
    index=index, 
    similarity_top_k=10,
)

# configure response synthesizer
response_synthesizer = ResponseSynthesizer.from_args(
    node_postprocessors=[
        SimilarityPostprocessor(similarity_cutoff=0.8)
    ]
)

# assemble query engine
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
)