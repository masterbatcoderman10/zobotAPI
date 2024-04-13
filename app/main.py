from fastapi import FastAPI, Request
from .utils import openai_secret
from pydantic import BaseModel
import logging
from openai import OpenAI
from typing import Optional, Dict, List

logging.basicConfig(level=logging.INFO)
openai_client = OpenAI(api_key=openai_secret)

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
    department_id: int
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

@app.post("/chat")
def chat(payload: ReqPayload):
    if not payload.message:
        return {"action": "reply", "replies": ["Hi, how can I help you today?"]}

    system_message = """You are WeBot, a helpful assistant that can answer questions, and provide information about our business.
    - Our Business name is SplitWireML
    - We offer excellent Machine Learning and AI services
    - We specialize in Natural Language Processing, in particular, chatbots powered by LLMs
    - We rely on a team of experts with years of experience in the field
    - We are always looking for new ways to improve our services
    - We have 3 pricing tiers : Basic, Pro, and Enterprise
    - We offer a free trial for all our services
    - We also offer a 30-day money-back guarantee
    - You can imagine the rest since this is a fictional company
    - Keep the answers precise and to the point"""

    message_text = payload.message.text

    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": message_text}
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        print(e)
        reply = "An error occurred while processing your request."

    return {"action": "reply", "replies": [reply]}