from fastapi import FastAPI
from pydantic import BaseModel

class Message(BaseModel):
    text: str

class Visitor(BaseModel):
    country: str
    time_zone: str
    email: str
    os: str
    department_id: str
    language: str
    channel: str

class Parameters(BaseModel):
    message: Message
    visitor: Visitor

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
def post_test():
    return {"action": "reply", "replies": ["Hello, World!"]}

@app.post("/echo")
def echo(params: Parameters):
    return {"action": "reply", "replies": [params.message.text]}