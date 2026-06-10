import os
import time
from fastapi import APIRouter, Request, Response, HTTPException
from agent import getResponse

router = APIRouter()

@router.get("/query", responses={404: {"description": "PDF file not found on disk"}})
async def queryRagSystem(request : Request, response : Response, fileName : str, query : str):
    # Check that the file exists on disk
    if not os.path.exists(fileName):
        raise HTTPException(status_code=404, detail=f"PDF file {fileName} does not exist")
    start = time.time()
    try:
        # Give the RAG agent the query, and wait for its answer
        result = await getResponse(fileName, query)
        # Determine the runtime, and add to header
        runtime = round(time.time() - start, 3)
        response.headers["X-Runtime"] = f"{runtime} seconds"
        # Return a JSON response
        return {"query": query, "response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))