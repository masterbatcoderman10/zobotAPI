from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
def post_test():
    return {"action": "reply", "replies": ["Hello, World!"]}

@app.post("/echo")
def echo():
    return {"action": "reply", "replies": ["Echo!"]}