from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mlflow
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from settings import Settings
import logging
from agent import get_agent
from validator import PromptRequest, AgentResponse

from langchain_core

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
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

agent = get_agent()

prompt = mlflow.genai.load_prompt(s.mflow_prompt_name)

app.get("/health")
async def health():
    return {"status" : "ok"}

@app.post("/agent", response_model=AgentResponse)
@limiter.limit("10/minute")
async def agent_answer(request : Request, body : PromptRequest):
    try:
        answer = await(agent.invoke(body.prompt))
        return AgentResponse(answer)
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Out of Time")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))