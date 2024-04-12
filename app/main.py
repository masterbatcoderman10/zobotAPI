from fastapi import FastAPI, Request
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)

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
    app_id: str

class ReqPayload(BaseModel):
    parameters: Parameters

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
    if not payload.parameters.message:
        return {"action": "reply", "replies": ["Hi, this is echo bot"]}
    return {"action": "reply", "replies": [payload.parameters.message.text]}