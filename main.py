# ======================================== Libs =================================
from model import graph
import asyncio
# ======================================== Function =============================
async def main():
    session_id = input("Enter your session id: ")
    config = {"configurable": {"thread_id": session_id}}
    while True:
        query = input("Enter query (quit - to quit) : ")
        if query == 'quit':
            break
        async for step in graph.astream(
                {"messages": [{"role": "user", "content": query}]},
                stream_mode="values",
                config=config,
        ):
            step["messages"][-1].pretty_print()


if __name__ == "__main__":
    asyncio.run(main())
