from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from query_engine import query_engine
from gpt4_query import query_gpt

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"])


@app.get("/")
async def root():
    return {"message": "Research GPT"}


@app.get("/papers")
def get_papers(prompt):
    res = query_engine.query(prompt)

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "Format this text to be more readable: " + res.response,
        },
    ]

    gpt_resp = query_gpt(messages)

    return gpt_resp
