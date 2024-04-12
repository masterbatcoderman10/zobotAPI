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
    message: Message = None
    visitor: Visitor

class ReqPayload(BaseModel):
    parameters: Parameters

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
def post_test():
    return {"action": "reply", "replies": ["Hello, World!"]}

@app.post("/echo")
def echo(payload: ReqPayload):
    #check if message is there or not
    if not payload.parameters.message:
        return {"action": "reply", "replies": ["Hi, this is echo bot"]}
    return {"action": "reply", "replies": [payload.parameters.message.text]}