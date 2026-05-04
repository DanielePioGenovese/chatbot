from fastmcp import FastMCP
from qdrant_client import models
import pprint

mcp = FastMCP('RAG', instructions='Provide a tool to use RAG with Qdrant')

@mcp.tool
def retrieve(query: str, collection_name: str, dense_model, sparse_model, late_model):
    
    prefetch = [
    models.Prefetch(
            query=models.Document(text=query, model=dense_model),
            using="dense",
            limit=20,
        ),
    models.Prefetch(
            query=models.Document(text=query, model=sparse_model),
            using="sparse",
            limit=20,
        ),
    ]
    
    results = client.query_points(
        collection_name,
        prefetch=prefetch,
        query=models.Document(text=query, model=late_model),
        using="multi",
        with_payload=True,
        limit=10,
    )

    return results

if __name__ == "__main__":
    mcp.run(transport='http', host='127.0.0.1', port=9000)
