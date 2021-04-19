from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello world!"}

@app.get("/method/{method}")
def method_check(method: str, response: Response):
    if method in methods:
        return f"message: {method}"
    else:
        response.status_code = status.HTTP_201_CREATED
    return f"message: {method}"
