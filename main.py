from fastapi import FastAPI

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
