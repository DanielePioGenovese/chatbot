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
        "mcpserver" : {
            "transport" : s.transport_settings,
            "url" : s.uri_mcp_server,
            'headers': {
                'X-Custom-Header': 'custom-value'
            }
        }
    }
)

async def get_agent(prompt):

    try:
        logger.info(f"Connecting to the MCP server: {s.uri_mcp_server} with transport {s.transport_settings}")
        tools = await client.get_tools()                                                        
        logger.info("MCP Tool loaded correctly!")
    except Exception as e:
        # exc_info=True stampa l'intero traceback dell'errore nei log di Docker
        logger.critical("Error loading the mcp server:", exc_info=True)
        raise e
    
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
        system_prompt=prompt
    )   

    return agent
