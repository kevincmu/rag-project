from fastapi import FastAPI
from endpoints import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(router)

# Implement CORS
origins = [
    "http://localhost:5173", # Default Vite port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def main():
    return {"message": "Hello World"}