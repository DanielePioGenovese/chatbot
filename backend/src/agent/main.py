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

# Instantiate the logger for this specific API module
logger = logging.getLogger(__name__)
# Initialize the application configuration object
s = Settings()

# Define global variables to hold the shared agent instance and system prompt template
agent = None 

# Define the lifespan context manager to manage application startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent, prompt
    # Set the remote tracking URI for the MLflow server
    mlflow.set_tracking_uri(s.uri_mlflow_server)
    
    # Construct the tracking URI to fetch the specific prompt version or alias from MLflow
    prompt_uri = f"prompts:/{s.mflow_prompt_name}@{s.mflow_prompt_alias}"  
    # Asynchronously download/load the tracked prompt from the MLflow Prompt Registry
    prompt = mlflow.genai.load_prompt(prompt_uri)
    logger.info(f"Main prompt loaded: {prompt_uri}")
    
    # Initialize the LangChain agent using the loaded system prompt template string
    agent = await get_agent(prompt.template)
    logger.info("Agent initialized successfully")
    # Yield control back to FastAPI; code after this runs when the application shuts down
    yield

# Initialize the FastAPI application instance with the designated lifespan handler
app = FastAPI(lifespan=lifespan)

# Initialize the rate limiter using the client's remote IP address as the identifier
limiter = Limiter(key_func=get_remote_address)
# Attach the limiter instance to the FastAPI application state
app.state.limiter = limiter
# Register the default exception handler to return a 429 error when limits are exceeded
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware to allow configured origins to interact with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=s.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Define a simple health check GET endpoint for infrastructure monitoring
@app.get("/health")                  
async def health():
    return {"status": "ok"}

import asyncio

# Define the primary agent interface POST endpoint with structural validation and a rate limit
@app.post("/agent", response_model=AgentResponse)
@limiter.limit("10/minute")
async def agent_answer(request: Request, body: PromptRequest):
    try:
        # Asynchronously invoke the LangChain agent with a 120-second hard timeout
        result = await asyncio.wait_for(
            agent.ainvoke({"messages": [HumanMessage(content=body.prompt)]}),
            timeout=120.0  
        )
        # Extract and return the text content from the last message in the agent's response history
        return AgentResponse(answer=result["messages"][-1].content)
    except asyncio.TimeoutError:
        # Raise a 504 Gateway Timeout error if the agent takes longer than 120 seconds to reply
        raise HTTPException(status_code=504, detail="Out of Time")
    except Exception as e:
        # Catch and log any other unhandled execution errors, then return a 500 Internal Server Error
        logger.exception("Agent error")
        raise HTTPException(status_code=500, detail=str(e))