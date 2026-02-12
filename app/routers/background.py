import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from services.main_process import pars_loop

@asynccontextmanager
async def lifespan(app: FastAPI):
    parser_task = asyncio.create_task(pars_loop())
    yield
    parser_task.cancel()

    try:
        await parser_task
    except asyncio.CancelledError:
        pass