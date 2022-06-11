from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse

from common.db import add_data

app = FastAPI()


class UpdateDTO(BaseModel):
    NPM: str
    name: str


@app.post("/update")
async def update(data: UpdateDTO):
    add_data(data.NPM, data.name)
    return JSONResponse({
        'status': 'OK'
    })


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
