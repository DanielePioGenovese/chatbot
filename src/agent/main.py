from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mlflow
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from settings import Settings
import logging
from agent import get_agent

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

prompt = mlflow.genai.load_prompt(s.mflow_prompt_name)

@app.get("/agent/{prompt}")
@limiter.limit("10/minute")
async def agent_answer(prompt : str):
    return await agent.invoke(prompt)