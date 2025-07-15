import uvicorn as uvicorn
from fastapi import FastAPI
from app.db.session import init_db
from app.routes.habit_route import habit_router
from app.routes.task_route import task_router
from app.routes.user_route import user_router

app = FastAPI()

@app.on_event("startup")
def start_db():
    init_db()

app.include_router(user_router)
app.include_router(task_router)
app.include_router(habit_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8002)