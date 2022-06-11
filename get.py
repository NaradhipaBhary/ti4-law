from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse

from common.db import get_data

app = FastAPI()


class UpdateDTO(BaseModel):
    NPM: str
    name: str


@app.get("/read/{npm}", response_model=UpdateDTO)
async def say_hello(npm: str):
    data = get_data(npm)
    return {
        "NPM": data.npm,
        "name": data.name
    }
