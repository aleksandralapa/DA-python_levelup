from fastapi import FastAPI, Response
from hashlib import sha512
from typing import Optional
from pydantic import BaseModel
from datetime import datetime, timedelta

app = FastAPI()
app.counter = 0
app.patients = [0]

class new_patient(BaseModel):
    name: str
    surname: str

class old_patient(BaseModel):
    id: int
    name: str
    surname: str
    register_date: str
    vaccination_date: str

#zad1.1
@app.get("/")
def root_view():
    return {"message": "Hello world!"}


#zad1.2
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

#zad1.3
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

#zad1.4
@app.post('/register', status_code=201)
def registration (new: new_patient):
    app.counter+=1
    date = datetime.today().strftime('%Y-%m-%d')
    old_patient.register_date = date
    x = len(new.name) + len(new.surname)
    date2 = datetime.today() + timedelta(days=x)
    date2 = date2.strftime('%Y-%m-%d')
    result = old_patient (id = app.counter, name = new.name, surname = new.surname, register_date = date, vaccination_date = date2)
    app.patients.append(result)
    return result

#zad1.5
@app.get('/patient/{id}', status_code=200)
def list_patient (response: Response, id: int):
    if id < 1:
        response.status_code = 400
        return
    if id > app.counter:
        response.status_code = 404
        return
    return app.patients[id]


