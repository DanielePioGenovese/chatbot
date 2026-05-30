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
client = MultiServerMCPClient({
    "mcpserver": {
        "transport": s.transport_settings,
        "url": s.uri_mcp_server,
        "headers": {"X-Custom-Header": "custom-value"}
    }
})

# Asynchronous function to initialize, wire up, and return the LangChain agent
async def get_agent(prompt):
    tools = await client.get_tools()
    llm = ChatOpenAI(
        model=s.model,
        base_url=s.uri_vllm,
        api_key='EMPTY', # Custom/vLLM endpoints often accept 'EMPTY' or placeholder keys
        temperature=s.temperature,
        timeout=s.timeout,
        streaming=s.streaming
        )
    agent = create_agent(model=llm, tools=tools, system_prompt=prompt)
    return agent
    