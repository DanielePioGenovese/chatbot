from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import mlflow
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from settings import Settings
import logging
from agent import get_agent
from validator import PromptRequest
from langchain_core.messages import HumanMessage, AIMessageChunk
from uuid import uuid4
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Instantiate the logger for this specific API module
logger = logging.getLogger(__name__)
# Initialize the application configuration object
s = Settings()

# Define global variables to hold the shared agent instance and system prompt template
prompt_template = None
# Define the lifespan context manager to manage application startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    global prompt_template
    # Set the remote tracking URI for the MLflow server
    mlflow.set_tracking_uri(s.uri_mlflow_server)
    
    # Construct the tracking URI to fetch the specific prompt version or alias from MLflow
    prompt_uri = f"prompts:/{s.mflow_prompt_name}@{s.mflow_prompt_alias}"  
    # Asynchronously download/load the tracked prompt from the MLflow Prompt Registry
    prompt = mlflow.genai.load_prompt(prompt_uri)
    logger.info(f"Main prompt loaded: {prompt_uri}")
    
    # Initialize the LangChain agent using the loaded system prompt template string
    # Yield control back to FastAPI; code after this runs when the application shuts down
    prompt_template = prompt.template
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
    allow_origins=["*"],
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
@app.post("/agent")
@limiter.limit("10/minute")
async def agent_answer(request: Request, body: PromptRequest):
    try:
        agent = await get_agent(prompt_template)
        config = {"configurable": {"thread_id": str(uuid4())}}

        async def token_generator():
            try:
                async for chunk in agent.astream(
                    {"messages": [HumanMessage(content=body.prompt)]},
                    config=config, 
                    stream_mode='messages'
                    ):
                         message_chunk, _ = chunk
                         if isinstance(message_chunk, AIMessageChunk):
                            content = message_chunk.content
                            if content and isinstance(content, str):
                                yield f'data: {json.dumps({"answer": content})}\n\n'   


            except Exception as e:
                        logger.exception("Error during streaming")
                        yield f"data: {json.dumps({'error': str(e)})}\n\n"
            finally:
                yield f"data: {json.dumps({'done': True})}\n\n"

        return StreamingResponse(
        token_generator(), 
        media_type="text/event-stream"
    )

    except asyncio.TimeoutError:
        # Raise a 504 Gateway Timeout error if the agent takes longer than 120 seconds to reply
        raise HTTPException(status_code=504, detail="Out of Time")
    except Exception as e:
        # Catch and log any other unhandled execution errors, then return a 500 Internal Server Error
        logger.exception("Agent error")
        raise HTTPException(status_code=500, detail=str(e))