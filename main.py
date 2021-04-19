from fastapi import FastAPI, Response, status

app = FastAPI()

@app.get("/")
def root_view():
    return {"message": "Hello World"}

methods = {"GET", "DELETE", "PUT", "OPTIONS"}

@app.get("/method/{method}")
def method_check(method: str, response: Response):
    if method in methods:
        return {"method": f"{method}"}
    elif method == "POST":
        response.status_code = status.HTTP_201_CREATED
    return {"method": f"{method}"}
