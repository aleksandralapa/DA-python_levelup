from fastapi import FastAPI, Response, Request
from hashlib import sha512
from typing import Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
from fastapi.templating import Jinja2Templates #wyk3

app = FastAPI()
app.counter = 0
app.patients = dict()

class new_patient(BaseModel):
    name: str
    surname: str

class old_patient(BaseModel):
    id: int
    name: str
    surname: str
    register_date: str
    vaccination_date: str

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
    if (not password) or (not password_hash):
        response.status_code = 401
        return
    password = password.encode(encoding = 'UTF-8', errors = 'ignore')
    password = sha512(password.strip()).hexdigest()
    if password != password_hash:
        response.status_code = 401
        return

#zad4
@app.post('/register', status_code=201)
def registration (new: new_patient):
    app.counter+=1
    date = datetime.today().strftime('%Y-%m-%d')
    old_patient.register_date = date
    len = new.name+new.surname
    x=0
    for i in len:
        if i.isalpha():
            x=x+1
    date2 = datetime.today() + timedelta(days = x)
    date2 = date2.strftime('%Y-%m-%d')
    result = old_patient (id = app.counter, name = new.name, surname = new.surname, register_date = date, vaccination_date = date2)
    app.patients[app.counter] = result
    return result
#zad5
@app.get('/patient/{id}', status_code=200)
def list_patent (response: Response, id: int):
    if id < 1:
        response.status_code = 400
        return
    if id > app.counter:
        response.status_code = 404
        return
    return app.patients[id]

#####zajęcia 3

templates = Jinja2Templates(directory="templates")

#zad 3.1
@app.get('/hello')
def greatings(request: Request):
    date = datetime.today().strftime('%Y-%m-%d')
    return templates.TemplateResponse("hello.html.j2", {"request": request, "date": date})



