import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

client = MultiServerMCPClient(
    {
        "rag" : {
            "transport" : "http",
            "url" : "http://mcpserver:6000"
        }
    }
)

async def main():

    tools = await client.get_tools()
    
    llm = ChatOpenAI(
        model=inference_settings.chat_model,
        base_url=inference_settings.vllm_base_url,
        api_key='EMPTY',
        temperature=0.2,
        timeout=120,
        streaming=True
    )
    
    agent = create_agent(
        model=llm,
        tools=tools,
        prompt='Connection to MLFLOW'
    )

    return agent

if _name_ == '_main_':
    asyncio.run(main())