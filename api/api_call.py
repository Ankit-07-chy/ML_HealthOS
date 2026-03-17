from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
from .gemini_model import LLM
# Add the current directory to path (helps Vercel find modules)
sys.path.append(os.path.dirname(__file__))
print("Current directory added to path:", os.path.dirname(__file__))
app = FastAPI(
    title="LLM Response API",
    description="Advanced API for LLM-based responses.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_instance = LLM()

class LLMRequest(BaseModel):
    input: str
    model: Optional[str] = "gemini-2.5-flash"


@app.get("/")
async def homepage():
    return {"message": "Welcome to the LLM Response API. Use /docs for API documentation."}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/llm")
async def llm_response(request: LLMRequest):
    try:
        response = llm_instance.full_implemented(request.input)
        return {"response": response}

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )