import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from settings import Settings
from fastapi import FastAPI
import mlflow
# Insert chatptompt template (the code does not work correctly)

app = FastAPI()
s = Settings()

mlflow.set_tracking_uri(s.uri_mflow_server)

client = MultiServerMCPClient(
    {
        "rag" : {
            "transport" : s.transport_settings,
            "url" : s.uri_mcp_server
        }
    }
)

prompt = mlflow.genai.load_prompt(s.mflow_prompt_name)

tools = client.get_tools()

# I will add the correct prompt format here

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
    prompt=s.mflow_prompt_name #Necessity to take the prompt from MLFLOW, this strategy is wrong
)   

@app.post("/agent/{prompt}")
async def agent_answer(prompt : str):

    return await agent.invoke(prompt)

if __name__ == '__main__':
    asyncio.run(agent_answer())