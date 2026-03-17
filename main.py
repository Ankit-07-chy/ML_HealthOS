# Importing From api_call.py to run the API
from api import app
import os

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable (for Hugging Face) or use default
    # Hugging Face expects port 7860
    port = int(os.getenv("PORT", 7860))
    
    # In production (Hugging Face), disable reload
    reload_enabled = os.getenv("ENVIRONMENT", "production") == "development"
    
    uvicorn.run(
        "api.api_call:app", 
        host="0.0.0.0", 
        port=port, 
        reload=reload_enabled
    )