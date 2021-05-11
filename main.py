from typing import Optional
import sqlite3
from fastapi import FastAPI, Request, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()

@app.get("/")
def root_view():
    return {"message": "Hello world!"}

@app.get('/categories')
async def cat(response: Response):
    categories = app.db_connection.execute("SELECT CategoryID, CategoryName FROM Categories ORDER BY CategoryID").fetchall()
    response.status_code = 200
    return {"categories": [{"id": i[0], "name": i[1]} for i in categories]}

@app.get('/customers')
async def cust(response: Response):
    customers = app.db_connection.execute("SELECT CustomerID, CompanyName, Address, PostalCode, City, Country FROM Customers ORDER BY CAST(CustomerID as INTEGER)").fetchall()
    response.status_code = 200
    adress = ['']*len(customers)
    index = 0
    for i in customers:
        i = list(i)
        for j in range(2, 6):
            if i[j] is None :
                i[j] = ''
            elif j<5:
                i[j]=i[j]+' '
            adress[index] = adress[index] + i[j]

        index += 1

    return {"customers": [{"id": customers[i][0], "name": customers[i][1], "full_adress": adress[i]} for i in range(len(customers))]}

