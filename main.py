from fastapi import FastAPI, Response, Request, Depends, Cookie #1;1;3;3;3
from hashlib import sha512
from typing import Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
from fastapi.templating import Jinja2Templates #wyk3
#do pd3
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import PlainTextResponse, HTMLResponse, RedirectResponse

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

#zad 3.2
sec = HTTPBasic()
app.login_session = ''
app.login_token = ''

@app.post('/login_session', status_code=201)
def session_authorization(response: Response, login_data: HTTPBasicCredentials = Depends(sec)):
    login = login_data.username
    password = login_data.password
    if login != "4dm1n" or password != 'NotSoSecurePa$$':
        response.status_code = 401
        return
    logs = login + password
    session_token = logs.encode(encoding = 'UTF-8', errors = 'ignore')
    session_token = sha512(session_token.strip()).hexdigest()
    response.set_cookie(key = "session_token", value = session_token)
    app.login_session = session_token

@app.post('/login_token', status_code=201)
def token_authorization(response: Response, login_data: HTTPBasicCredentials = Depends(sec)):
    login = login_data.username
    password = login_data.password
    if login != "4dm1n" or password != 'NotSoSecurePa$$':
        response.status_code = 401
        return
    logs = login + password
    token_value = logs.encode(encoding = 'UTF-8', errors = 'ignore')
    token_value = sha512(token_value.strip()).hexdigest()
    app.login_token = token_value
    return {"token": token_value}


#zad3.3
#zad3.3
@app.get("/welcome_session")
def swelcome(response: Response, format: Optional[str] = None, session_token: str = Cookie(None)):
    if session_token != app.login_session:
        response.status_code = 401
        return
    if format == "json":
        return {"message": "Welcome!"}
    elif format == "html":
        return HTMLResponse(content="<h1>Welcome!</h1>")
    else:
        return PlainTextResponse("Welcome!")

@app.get("/welcome_token")
def twelcome(response: Response, token: str = '', format: str = ''):
    if (token == '') or (token != app.login_token):
        response.status_code = 401
        return
    if format == "json":
        return {"message": "Welcome!"}
    elif format == "html":
        return HTMLResponse(content="<h1>Welcome!</h1>")
    else:
        return PlainTextResponse("Welcome!")
    
    #zad3.4
@app.delete("/logout_session")
def slogout(response: Response, format: Optional[str] = None, session_token: str = Cookie(None)):
    if session_token != app.login_session:
        response.status_code = 401
        return
    app.login_session = ''
    return RedirectResponse(url = "/logged_out?format=" + format, status_code=303)


@app.delete("/logout_token")
def tlogout(response: Response, token: str = '', format: str = ''):
    if (token == '') or (token != app.login_token):
        response.status_code = 401
        return
    app.login_token = ''
    return RedirectResponse(url = "/logged_out?format=" + format, status_code = 303) 


@app.get("/logged_out", status_code=200)
def logged_out(format: str = ''):
    if format == "json":
        return {"message": "Logged out!"}
    elif format == "html":
        return HTMLResponse(content="<h1>Logged out!</h1>")
    else:
        return PlainTextResponse("Logged out!")
