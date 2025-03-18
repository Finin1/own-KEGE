from typing import Any
from uvicorn import run
from fastapi import FastAPI
from pathlib import Path
from flask import Flask
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI(root_path="/api")
f_app = Flask(__name__)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/task/{num}")
async def get_number(num: int):
    response: dict[str, Any] = {}
    response["number"] = num
    path_to_template = Path("template", f"task{num}.html")
    response["content"] = open(path_to_template, encoding="utf-8").readline()
    return response


if __name__ == "__main__":
    # f_app.run(host="0.0.0.0", port=8080)
    run(app=app, host="0.0.0.0", port=8080)
