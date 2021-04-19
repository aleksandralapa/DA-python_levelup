from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello world!"}

@app.get("/method/{method}")
def get_method(metohod):
    return f"message {method}"
