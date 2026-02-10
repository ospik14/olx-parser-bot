from fastapi import FastAPI
from routers import commands, background

app = FastAPI(lifespan=background.lifespan)

app.include_router(router=commands.router)