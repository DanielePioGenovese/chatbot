from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse
from qdrant_client import QdrantClient, models
import logging
import time
from settings import Settings
import mlflow

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load settings
s = Settings()

# Initialize Qdrant Client
client = QdrantClient(host=s.qdrant_host, port=s.qdrant_port)

prompt_uri = f"prompts:/{s.mlflow_prompt_name}@{s.mlflow_prompt_alias}"  
prompt = mlflow.genai.load_prompt(prompt_uri)

instructions_text = prompt.template

# Initialize FastMCP Server
mcp = FastMCP("RAG")

@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request):
    """Health check endpoint."""
    return JSONResponse({"status": "ok"})

@mcp.tool(
    name="find_relevant_documents",
    description=(
        instructions_text
    )
)                      
async def retrieve(query: str) -> list:
    """
    Returns a list of docs using vector search on Qdrant.

    Args:
        query: The user's question or search intent.
        collection_name: The target collection name (default is 'small_metal_parts').
        
    Returns:
        A list of raw document payloads matching the query.
    """
    
    logger.info(f"Starting Qdrant dense search for query: '{query}'")
    start_time = time.time()

    # Fast single-stage dense retrieval (Sparse and Late Interaction removed for performance)
    results = client.query_points(
        collection_name='small_metal_parts',
        prefetch=[
            models.Prefetch(
                query=models.Document(text=query, model=s.dense_model),
                using="dense",
                limit=10,
            ),
            models.Prefetch(
                query=models.Document(text=query, model=s.sparse_model),
                using="sparse",
                limit=10,
            ),
        ],
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        with_payload=True,
        limit=5,
)

    end_time = time.time()
    logger.info(f"Qdrant responded in {end_time - start_time:.2f} seconds")

    points = list(results.points) 
    return [point.payload for point in points]

if __name__ == "__main__":
    logger.info(f"Starting MCP server on {s.host}:{s.port}")
    mcp.run(transport="http", host=s.host, port=s.port)