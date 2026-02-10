import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from services.main_process import pars_loop
from dependencies import db_dep

@asynccontextmanager
async def lifespan(app: FastAPI, db: db_dep):
    
    parser_task = asyncio.create_task(pars_loop(db))
    yield
    parser_task.cancel()