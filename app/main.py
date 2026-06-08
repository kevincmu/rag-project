from fastapi import FastAPI
from endpoints import router

app = FastAPI()
app.include_router(router)

# Start app with uvicorn app.main:app --reload