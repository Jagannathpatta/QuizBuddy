from fastapi import APIRouter
from sqlalchemy import false
from Quiz.database import *
from Quiz.dbmodels import *

router = APIRouter(
    prefix="/student",
    tags=["student"],
    responses={404: {"description": "Not found"}},
)

@router.post("/createStudent")
def create_student( stud:Student ):
    conn = get_db()
    curr= conn.cursor()
    try:        
        query = "insert into Students( Name, email, password, phone, points, Score , Performance_lvl ) values('"+ str(stud.name) + "','" + stud.email + "','" + str(stud.password) +"','" + str(stud.phone) +"',"+ str(stud.point) +","+ str(stud.score) +",'"+ stud.performance_lvl +"')"
        print("query",query)
        curr.execute(query)

        conn.commit()
        return {"status":"success", "msg": "Successfuly User Created" , "res": stud}
    except Exception as e :
        conn.rollback()    
        return {"status":"unsuccess", "msg": format(e) }
    finally:
        curr.close()
        close_db(conn)

@router.post("/profile")
def profile( id:int ):
    conn = get_db()
    curr= conn.cursor()   
    try:        
        query = "select * from Students where St_id = "+ str(id)
        curr.execute(query)    
        res = [dict((curr.description[i][0], value) \
                for i, value in enumerate(row)) for row in curr.fetchall()]
        curr.close()
        close_db(conn)
        return {"status":"success", "msg": "Successfuly Read" , "res":res}
    except Exception as e :   
        return {"status":"unsuccess", "msg": format(e) }
    finally:
        curr.close()
        close_db(conn)

@router.post("/generatequiz", tags=["quiz"])
def generate_quiz():
    conn = get_db()
    curr= conn.cursor()
    try:
        # Yet to compelete
        conn.commit()
        return {"status":"success", "msg": "Successfuly Qustions Created" , "res": quests}
    except Exception as e :
        conn.rollback()    
        return {"status":"unsuccess", "msg": format(e) }
    finally:
        curr.close()
        close_db(conn)