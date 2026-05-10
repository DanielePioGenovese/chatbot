import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from settings import Settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mlflow
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI()
s = Settings()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = Limiter()
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
mlflow.set_tracking_uri(s.uri_mflow_server)

app.add_middleware(
    CORSMiddleware,
    allow_origins=s.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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

@app.get("/agent/{prompt}")
@limiter.limit("10/minute")
async def agent_answer(prompt : str):
    return await agent.invoke(prompt)


if __name__ == '__main__':
    asyncio.run(agent_answer())