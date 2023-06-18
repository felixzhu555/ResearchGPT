from llama_index import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    GPTVectorStoreIndex,
    LLMPredictor,
    ServiceContext,
    ResponseSynthesizer,
    Document,
)
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.indices.postprocessor import SimilarityPostprocessor
from langchain import OpenAI
import time
import os
from tqdm import tqdm
from pypdf import PdfReader

# # define LLM
# llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="text-davinci-003"))
# print("LLM created")

# # configure service context
# service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
# print("service context created")


def reset_eof_of_pdf_return_stream(pdf_stream_in):
    for i, x in enumerate(pdf_stream_in[::-1]):
        actual_line = len(pdf_stream_in)
        if b"%%EOF" in x:
            actual_line -= i
            break
    return pdf_stream_in[:actual_line]


start = time.time()
# documents = SimpleDirectoryReader("/Users/felix_3gpdyfd/ai hackathon/data").load_data()
documents = []
for filename in tqdm(os.listdir("/Users/felix_3gpdyfd/ai hackathon/data")):
    fname = "/Users/felix_3gpdyfd/ai hackathon/data/" + filename
    try:
        reader = PdfReader(fname)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        documents.append(Document(text))
    except:
        pass

print(f"{len(documents)} documents created", time.time() - start)

# build index
# index = VectorStoreIndex.from_documents(documents)
index = GPTVectorStoreIndex.from_documents(documents)
print("vector index created", time.time() - start)

index.storage_context.persist(persist_dir="persist_index")
print("index saved to disk", time.time() - start)

# configure retriever
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10,
)
print("retriever created", time.time() - start)

# configure response synthesizer
response_synthesizer = ResponseSynthesizer.from_args(
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.85)]
)
print("response synthesizer created", time.time() - start)

# assemble query engine
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
)
print("query engine created", time.time() - start)

# query_engine = index.as_query_engine()
query = "respond to this query: what papers are there about deep learning for music? give a quick summary for each of them."
# response = query_engine.query(query)
fullResponse = ""
resp = None
while True:
    resp = query_engine.query(query + "\n\n" + fullResponse)
    print("response received", time.time() - start)
    if resp and resp.response and resp.response != "Empty Response":
        fullResponse += " " + resp.response
    else:
        break

with open("output.txt", "w") as f:
    f.write(fullResponse + "\n\n" + resp.get_formatted_sources())
