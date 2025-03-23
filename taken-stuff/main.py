from os import listdir
from pathlib import Path
from flask import Flask, render_template
# from api import app as api_app

app = Flask(__name__)

@app.route("/train")
def train():
    return "\n".join(open("train.htm", encoding="utf-8").readlines())
    # return "hello, world"


@app.get("/generate")
def generate_var():
    response = {}
    response["varId"] = 1
    topics = []
    numbers = listdir("template")
    for number in numbers:
        new_topic = {}
        new_topic["ege_id"] = number.replace("task", "").replace(".html", "")
        path_to_number = Path("template", number)
        new_topic["content"] = open(path_to_number, encoding="utf-8").readline()
        new_topic["answer"] = "0"
        topics.append(new_topic)
    response["topics"] = topics
    
    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
