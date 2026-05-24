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

# Instantiate the logger for this specific module
logger = logging.getLogger(__name__)
# Initialize the application configuration object
s = Settings()

# Configure the MultiServerMCPClient with connection details specified in the settings
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

# Asynchronous function to initialize, wire up, and return the LangChain agent
async def get_agent(prompt):

    try:
        logger.info(f"Connecting to the MCP server: {s.uri_mcp_server} with transport {s.transport_settings}")
        # Asynchronously fetch the dynamically exposed tools from the connected MCP server
        tools = await client.get_tools()                                                        
        logger.info("MCP Tool loaded correctly!")
    except Exception as e:
        # exc_info=True stampa l'intero traceback dell'errore nei log di Docker
        logger.critical("Error loading the mcp server:", exc_info=True)
        raise e
    
    # Set up the Language Model configuration pointing to a custom vLLM endpoint
    llm = ChatOpenAI(
        model=s.model,
        base_url=s.uri_vllm,
        api_key='EMPTY', # Custom/vLLM endpoints often accept 'EMPTY' or placeholder keys
        temperature=s.temperature,
        timeout=s.timeout,
        streaming=s.streaming
    )

    # Bind the configured LLM, fetched MCP tools, and the passed system instructions into an agent instance
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=prompt
    )   

    # Return the executable agent instance
    return agent