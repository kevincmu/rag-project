import os
import markdown
import time
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from agent import getResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/query/", responses={404: {"description": "PDF file not found on disk"}}, response_class=HTMLResponse)
async def queryRagSystem(request : Request, fileName : str, query : str):
    # Check that the file exists on disk
    if not os.path.exists(fileName):
        raise HTTPException(status_code=404, detail=f"PDF file {fileName} does not exist")
    start = time.time()
    try:
        # Give the RAG agent the query, and wait for its answer
        result = await getResponse(fileName, query)
        # Convert the markdowned result to HTML
        htmlResult = markdown.markdown(result)
        # Construct the HTML template
        response = templates.TemplateResponse(
            "template.html", 
                {"request": request, 
                "query": query, 
                "response": htmlResult
                }
            )
        # Determine the runtime, and add to header
        runtime = round(time.time() - start, 3)
        response.headers["X-Runtime"] = f"{runtime} seconds"
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))