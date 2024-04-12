from fastapi import FastAPI, Request
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)

from pydantic import BaseModel
from typing import Optional, Dict, List

class Location(BaseModel):
    country: str

class Message(BaseModel):
    meta: Dict = None
    text: str
    type: str = "text"

class Visitor(BaseModel):
    active_conversation_id: str
    country_code: str
    country: str
    os: str
    department_id: str
    channel: str
    language: str
    time_zone: str
    email: str

class RequestModel(BaseModel):
    os: str
    location: Location
    id: str
    app_id: str

class ReqPayload(BaseModel):
    handler: str = None
    request: RequestModel = None
    attachments: List = None
    org_id: str = None
    message: Message = None
    visitor: Visitor = None
    operation: str = None

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log the request method and URL
    logging.info(f"{request.method} {request.url}")
    
    # Log the request headers
    logging.info("Headers:")
    for name, value in request.headers.items():
        logging.info(f"{name}: {value}")
    
    # Log the request body (only for POST requests)
    if request.method == "POST":
        body = await request.json()
        logging.info("Body:")
        logging.info(body)
    
    # Call the next middleware or route handler
    response = await call_next(request)
    
    # Optionally, log the response status code
    logging.info(f"Response status code: {response.status_code}")
    
    return response


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
def post_test(request: Request):
    return {"action": "reply", "replies": ["Hello, World!"]}

@app.post("/echo")
def echo(payload: ReqPayload):
    #check if message is there or not
    if not payload.message:
        return {"action": "reply", "replies": ["Hi, this is echo bot"]}
    return {"action": "reply", "replies": [payload.message.text]}