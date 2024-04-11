from fastapi import FastAPI

app = FastAPI()

@app.post("/")
def read_root():
    return {"action": "reply", "replies": ["Hello, World!"]}

@app.post("/echo")
def read_item():
    return {"action": "reply", "replies": ["Echo!"]}