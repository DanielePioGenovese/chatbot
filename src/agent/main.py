import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from settings import Settings

s = Settings()

client = MultiServerMCPClient(
    {
        "rag" : {
            "transport" : s.transport_settings,
            "url" : s.uri_mcp_server
        }
    }
)

async def main():

    tools = await client.get_tools()
    
    llm = ChatOpenAI(
        model=s.model,
        base_url=s.uri_mcp_server,
        api_key='EMPTY',
        temperature=s.temperature,
        timeout=s.timeout,
        streaming=s.streaming
    )
    
    agent = create_agent(
        model=llm,
        tools=tools,
        prompt='Connection to MLFLOW'
    )

    return agent

if __name__ == '_main_':
    asyncio.run(main())