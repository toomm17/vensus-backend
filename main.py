from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import database, metadata, engine
from user.api import user_router

app = FastAPI()

app.state.database = database

origins = [
    'https://localhost:8080',
    'http://localhost:8080',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.on_event('startup')
async def startup() -> None:
    database_ = app.state.database
    metadata.create_all(engine)
    if not database_.is_connected:
        await database_.connect()
        
        
@app.on_event('shutdown')
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


app.include_router(user_router)