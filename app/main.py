import uvicorn as uvicorn
from fastapi import FastAPI
from app.db.session import init_db

app = FastAPI()

@app.on_event("startup")
def start_db():
    init_db()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8002)