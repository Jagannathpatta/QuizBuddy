from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Quiz.dbmodels import *
from Quiz.database import *

from internal import admin
from routers import students , institute

app = FastAPI()

origins = [    
    "http://localhost",
    "http://localhost:3000",    
    "https://quizbuddyspit.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)
app.include_router(students.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/register")
def create_std(std:Student):
    conn = get_db()
    
    curr= conn.cursor()
   
    curr.execute("select * from users")
    
    res = [dict((curr.description[i][0], value) \
               for i, value in enumerate(row)) for row in curr.fetchall()]
    close_db(conn)
    return {"status":"success", "msg": "Successfuly Registered" , "res":res}

@app.post("/create_class")
def create_class(cls:Class):
    conn = get_db()
    curr= conn.cursor()
    query = "insert into users(name) values('"+cls.name+"')"
    print("query",query)
    curr.execute(query)
    conn.commit()
    # res = [dict((curr.description[i][0], value) \
    #            for i, value in enumerate(row)) for row in curr.fetchall()]
    close_db(conn)
    return {"status":"success", "msg": "Successfuly Created"}

@app.put("/update_class")
def create_class(cls:Class):
    conn = get_db()
    curr= conn.cursor()
    query = "update users SET name = '"+ cls.name +"' where id = "+ str(cls.id) 
    print("query",query)
    curr.execute(query)
    conn.commit()
    close_db(conn)
    return {"status":"success", "msg": "Successfuly Updated"}

@app.delete("/delete_class/{id}")
def delete_class(id:int):
    conn = get_db()
    curr= conn.cursor()
    query = "delete from users where id = "+ str(id) 
    print("query",query)
    curr.execute(query)
    conn.commit()
    close_db(conn)
    return {"status":"success", "msg": "Successfuly deleted"}