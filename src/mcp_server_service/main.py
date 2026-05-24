from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse
from qdrant_client import QdrantClient, models
import logging
import time
from settings import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load settings
s = Settings()

# Initialize Qdrant Client
client = QdrantClient(host=s.qdrant_host, port=s.qdrant_port)

# Initialize FastMCP Server
mcp = FastMCP("RAG", instructions="Provide a tool to use RAG with Qdrant")

@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request):
    """Health check endpoint."""
    return JSONResponse({"status": "ok"})

@mcp.tool(
    name="find_relevant_documents",
    description=(
        "Prompt by MLFlow"
    )
)                      
def retrieve(query: str, collection_name: str = "small_metal_parts") -> list:
    """
    Performs a fast dense vector search on Qdrant.

    Args:
        query: The user's question or search intent.
        collection_name: The target collection name (default is 'small_metal_parts').
        
    Returns:
        Make a summary to answer to the user question from the retrieved documents.
    """
    
    logger.info(f"Starting Qdrant dense search for query: '{query}'")
    start_time = time.time()

    # Fast single-stage dense retrieval (Sparse and Late Interaction removed for performance)
    results = client.query_points(
        collection_name='small_metal_parts',
        query=models.Document(text=query, model=s.dense_model),
        using="dense",
        with_payload=True,
        limit=3,
    )

    end_time = time.time()
    logger.info(f"Qdrant responded in {end_time - start_time:.2f} seconds")

    return [point.payload for point in results.points]

if __name__ == "__main__":
    logger.info(f"Starting MCP server on {s.host}:{s.port}")
    mcp.run(transport="http", host=s.host, port=s.port)