from fastapi import FastAPI, HTTPException
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
    if data is None:
        raise HTTPException(status_code=404, detail="No data found with specified NPM")
    return {
        "NPM": data.npm,
        "name": data.name
    }
