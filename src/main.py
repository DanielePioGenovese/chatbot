from pydantic_ai import Agent, RunContext
import asyncio
from dataclasses import dataclass
from qdrant_client import QdrantClient

@dataclass
class Deps:
    qdrant: QdrantClient
    collection_name: str

# Using VLLM as a service

agent = Agent(
    model="meta-llama/Llama-3.2-3B-Instruct",
    base_url='http://localhost:8000/v1',
    api_key='vllm-is-free'
)

@agent.tool
async def retrive_documents(ctx: RunContext[Deps], search_query: str) ->  str:

    search_result = ctx.deps.qdrant.query_points(
        collection_name=ctx.deps.collection_name,
        query=search_query,
        limit=3
    )


async def main():

    # result = await agent.run('What is the capital of italy?')
    # print(result.output)

    async with agent.run_stream('What is the capital of italy?') as response:
        async for text in response.stream_text():
            print(text)
    

            

if __name__ == "__main__":
    asyncio.run(main())
