from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import mlflow
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from settings import Settings
import logging
from agent import get_agent
from validator import PromptRequest, AgentResponse
from langchain_core.messages import HumanMessage

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
s = Settings()

agent = None 

@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent, prompt
    mlflow.set_tracking_uri(s.uri_mlflow_server)
    
    prompt_uri = f"prompts:/{s.mflow_prompt_name}@{s.mflow_prompt_alias}"  
    prompt = mlflow.genai.load_prompt(prompt_uri)
    logger.info(f"Prompt loaded: {prompt_uri}")
    
    agent = await get_agent()
    logger.info("Agent initialized successfully")
    yield
app = FastAPI(lifespan=lifespan)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=s.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")                  
async def health():
    return {"status": "ok"}

import asyncio

@app.post("/agent", response_model=AgentResponse)
@limiter.limit("10/minute")
async def agent_answer(request: Request, body: PromptRequest):
    try:
        result = await asyncio.wait_for(
            agent.ainvoke({"messages": [HumanMessage(content=body.prompt)]}),
            timeout=120.0  
        )
        return AgentResponse(answer=result["messages"][-1].content)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Out of Time")
    except Exception as e:
        logger.exception("Agent error")
        raise HTTPException(status_code=500, detail=str(e))