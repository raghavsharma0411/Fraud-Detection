"""
Generative AI endpoints.
"""
from typing import Dict, Any
from fastapi import APIRouter

router = APIRouter()


@router.get("/models")
async def list_genai_models() -> Dict[str, Any]:
    """List available GenAI models."""
    return {"models": [], "message": "GenAI endpoints ready for implementation"}


@router.post("/chat")
async def chat_completion(data: Dict[str, Any]) -> Dict[str, Any]:
    """Chat completion endpoint."""
    return {"message": "Chat endpoint ready for implementation", "data": data}