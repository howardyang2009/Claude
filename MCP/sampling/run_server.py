import uvicorn
from server import mcp

if __name__ == "__main__":
    uvicorn.run(
        mcp.streamable_http_app(),
        host="0.0.0.0",
        port=3000,
    )