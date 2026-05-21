from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse
from qdrant_client import QdrantClient, models
import logging
from settings import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

s = Settings()

client = QdrantClient(host=s.qdrant_host, port=s.qdrant_port)

mcp = FastMCP("RAG", instructions="Provide a tool to use RAG with Qdrant")

@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request):
    return JSONResponse({"status": "ok"})

@mcp.tool(
        name="find_relevant_documents",
        description="Retrieves technical and company-specific documents from the Qdrant database. "
        "YOU MUST USE THIS TOOL to answer any questions about company policies, "
        "metal part specifications, production processes, or internal documentation. "
        "Do not answer based on your internal knowledge for company-specific queries; "
        "always fetch the latest data using this tool first."
)                      
def retrieve(query: str, collection_name: str = "small_metal_parts") -> list:
    """
    Performs a hybrid search (dense + sparse) on Qdrant.

    Args:
        query: The user's question or search intent.
        collection_name: The target collection name (e.g., 'small_metal_parts').
        
    Returns:
        A list of payloads retrieved from Qdrant. Use the content of these payloads 
        to formulate a grounded and accurate response to the user.
    """
    
    prefetch = [
        models.Prefetch(
            query=models.Document(text=query, model=s.dense_model),
            using="dense",
            limit=20,
        ),
        models.Prefetch(
            query=models.Document(text=query, model=s.sparse_model),
            using="sparse",
            limit=20,
        ),
    ]

    results = client.query_points(
        "small_metal_parts",
        prefetch=prefetch,
        query=models.Document(text=query, model=s.late_model),
        using="multi",
        with_payload=True,
        limit=10,
    )

    return [point.payload for point in results.points]

if __name__ == "__main__":
    logger.info(f"Starting MCP server on {s.host}:{s.port}")
    mcp.run(transport="http", host=s.host, port=s.port)