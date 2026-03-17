# Importing From api_call.py to run the API
from api import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.api_call:app", host="0.0.0.0", port=8000, reload=True)

