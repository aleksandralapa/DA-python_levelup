from fastapi import FastAPI, Response
from hashlib import sha512
from typing import Optional

app = FastAPI()


#zad1
@app.get("/")
def root_view():
    return {"message": "Hello world!"}


#zad2
@app.get("/method")
def GET():
    return {"method": "GET"}

@app.delete("/method")
def DELETE():
    return {"method": "DELETE"}

@app.put("/method")
def PUT():
    return {"method": "PUT"}

@app.options("/method")
def OPTIONS():
    return {"method": "OPTIONS"}

@app.post("/method", status_code = 201)
def POST():
    return {"method": "POST"}

#zad3
@app.get('/auth', status_code=204)
def password_check(response: Response, password: Optional[str] = None, password_hash: Optional[str] = None):
    password = password.encode(encoding = 'UTF-8', errors = 'ignore')
    password = sha512(password.strip()).hexdigest()
    if (password != password_hash) or (not password) or (not password_hash):
        response.status_code = 401
        return
