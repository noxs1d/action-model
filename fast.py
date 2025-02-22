from fastapi import FastAPI
from model import graph

app = FastAPI(
    title="Action Model",
    description="LLM for CS ",
    version="1.0"
)

@app.post("/run")
async def run(thread_id, query):
    config = {"configurable": {"thread_id": thread_id}}
    response = await graph.ainvoke(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="values",
        config=config,
    )
    return response["messages"][-1].dict()["content"]
