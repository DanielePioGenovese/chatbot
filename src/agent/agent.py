import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from settings import Settings
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
s = Settings()


client = MultiServerMCPClient(
    {
        "rag" : {
            "transport" : s.transport_settings,
            "url" : s.uri_mcp_server
        }
    }
)

async def get_agent():
    tools = await client.get_tools()
    logger.info("MCP Tool loaded correctly!")
    
    llm = ChatOpenAI(
        model=s.model,
        base_url=s.uri_vllm,
        api_key='EMPTY',
        temperature=s.temperature,
        timeout=s.timeout,
        streaming=s.streaming
    )

    agent = create_agent(
        model=llm,
        tools=tools,
        prompt=s.mflow_prompt_name
    )   

    return agent
