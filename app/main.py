from fastapi import FastAPI
from routers import commands

app = FastAPI()

app.include_router(router=commands.router)