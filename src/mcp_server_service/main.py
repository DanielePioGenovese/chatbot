from fastmcp import FastMCP
from qdrant_client import QdrantClient, models
from pydantic_settings import BaseSettings
import logging
from settings import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



s = Settings()

client = QdrantClient(host=s.qdrant_host, port=s.qdrant_port)

mcp = FastMCP("RAG", instructions="Provide a tool to use RAG with Qdrant")

@mcp.tool()                      
def retrieve(query: str, collection_name: str) -> list:
    """Retrieve relevant documents using hybrid search."""
    
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
        collection_name,
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