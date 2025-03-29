import os
from typing import Any
from pathlib import Path
from flask import Flask

app = Flask(__name__)


@app.get("/task/<int:num>")
def get_number(num: int):
    response: dict[str, Any] = {}
    response["number"] = num
    path_to_template = Path("template", f"task{num}.html")
    response["content"] = open(path_to_template, encoding="utf-8").readline()
    return response


if __name__ == "__main__":
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 8080))
    app.run(host=host, port=port)
