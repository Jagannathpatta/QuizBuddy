from urllib.request import Request
from fastapi import APIRouter
import requests
import json
from datetime import datetime
import random
from sqlalchemy import false
from Quiz.database import *
from Quiz.dbmodels import *

router = APIRouter(
    prefix="/student",
    tags=["student"],
    responses={404: {"description": "Not found"}},
)

@router.post("/login")
def login( email : str ):
    conn = get_db()
    curr= conn.cursor()   
    try:        
        query = "select * from Students where email = '"+ email + "'"
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
def generate_quiz( quiz : Quiz):
    conn = get_db()
    curr= conn.cursor()
    try:
        # Yet to compelete
        print( quiz.sid , quiz.cid , quiz.subid , quiz.chid )
        query = "select `Performance_lvl` from Students where St_id = "+ str(quiz.sid)
        curr.execute(query)
        pef_lvl = curr.fetchone()[0]
        if pef_lvl == '1':
            nlow = 10
            nmid = 6
            nhig = 4
        elif pef_lvl == '2':
            nlow = 6
            nmid = 10
            nhig = 4
        elif pef_lvl == '3':
            nlow = 4
            nmid = 6
            nhig = 10

        query = "insert into Quiz( `n_high_lvl`, `n_mod_lvl`, `n_low_lvl`, `stud_cat` ) values("+ str(nhig) + "," + str(nmid) + "," + str(nlow) +",'" + pef_lvl +"')"
        curr.execute(query)
        curr.execute('SELECT LAST_INSERT_ID()')
        quiz_id = curr.fetchone()[0]

        filterLow = {  "cid": quiz.cid, "sid": quiz.subid, "CHid": quiz.chid, "dificulty_lvl": "1" }
        filterMid = {  "cid": quiz.cid, "sid": quiz.subid, "CHid": quiz.chid, "dificulty_lvl": "2" }
        filterHig = {  "cid": quiz.cid, "sid": quiz.subid, "CHid": quiz.chid, "dificulty_lvl": "3" }
                      
        get_question= f"https://2m0x0d.deta.dev/student/problems"
                
        get_question_response = requests.post(get_question , json=filterLow)
        if get_question_response.status_code == 200:
            res = json.loads(get_question_response.content.decode('utf-8'))
            print("low",res)
            lowQuests = random.sample( res['res'] , nlow )
            for question in lowQuests:
                curr.execute("insert into Quiz_questions(`Quiz_id` , `qid` , `q_dificulty`) values (" + str(quiz_id) + " , " + str(question["qid"]) +" , 1)")
               
        get_question_response = requests.post(get_question , json=filterMid)
        if get_question_response.status_code == 200:
            res = json.loads(get_question_response.content.decode('utf-8'))
            print("mid",res)
            midQuests = random.sample( res['res'] , nmid )
            for question in midQuests:
                curr.execute("insert into Quiz_questions(`Quiz_id` , `qid` , `q_dificulty`) values (" + str(quiz_id) + " , " + str(question["qid"]) +" , 2)")
                
        get_question_response = requests.post(get_question , json=filterHig)
        if get_question_response.status_code == 200:
            res = json.loads(get_question_response.content.decode('utf-8'))
            print("hig",res)
            higQuests = random.sample( res['res'] , nhig )
            for question in higQuests:
                curr.execute("insert into Quiz_questions(`Quiz_id` , `qid` , `q_dificulty`) values (" + str(quiz_id) + " , " + str(question["qid"]) +" , 3)")
                
        conn.commit()
        return {"status":"success", "msg": "Successfuly Quiz Created" , "quiz_id" : quiz_id ,"timeInMins":30 , "noQuestions":20 ,"lowQuests": lowQuests , "midQuests": midQuests , "higQuests": higQuests }
    except Exception as e :
        conn.rollback()    
        return {"status":"unsuccess", "msg": format(e) }
    finally:
        curr.close()
        close_db(conn)

@router.post("/startQuiz", tags=["quiz"])
def startQuiz( req : StudQuizId ):
    conn = get_db()
    curr= conn.cursor()   
    try:       
        finalres = []
        query0 = "select `qid` from Quiz_questions where Quiz_id = "+ str(req.quiz_id)
        curr.execute(query0)
        for qid in curr.fetchall() :            
            query = "select * from Questions where qid = "+ str(qid[0])
            curr.execute(query)    
            res = [dict((curr.description[i][0], value) \
                    for i, value in enumerate(row)) for row in curr.fetchall()]
                       
            query1 = "select `Oid`, `option`, `type` from Options where qid = "+ str(qid[0])
            curr.execute(query1)    
            res1 = [dict((curr.description[i][0], value) \
                    for i, value in enumerate(row)) for row in curr.fetchall()]
            res[0]['Options'] = res1
            finalres.append(res[0])
        
        return {"status":"success", "msg": "Successfuly Read" , "res":finalres}
    except Exception as e :   
        return {"status":"unsuccess", "msg": format(e) }
    finally:
        curr.close()
        close_db(conn)

@router.post("/problems")
def problems( filters : Problem ):
    conn = get_db()
    curr= conn.cursor()
    try:               
        query = """ 
                select q.qid, e.Class, e.Subject, e.Chapter , q.question , q.dificulty_lvl from ( select d.*, cp.Chapter , cp.CHid
                from (select c.Class, c.Cid, s.Subject, s.sid 
                    from Classes c inner join Subjects s on c.Cid = s.Cid) d 
                    inner join Chapters cp on cp.Sid = d.Sid ) e
                    inner join Questions q on q.CHid = e.CHid 
         """
        filt = ""
        for i,v in filters:
            print(i,v)
            if int(v) > 0 :  
                if i != "dificulty_lvl" :
                    filt = filt + "e."+i + "=" + str(v) + " and "  
                else:
                    filt = filt + "q."+i + "= '" + str(v) + "'"
        if filt:
            if filt[-4:] == 'and ':
                query = query + " where " + filt[:-4]
            else:
                query = query + " where " + filt

        print(query)
        curr.execute(query)    
        res = [dict((curr.description[i][0], value) \
                for i, value in enumerate(row)) for row in curr.fetchall()]
        curr.close()
        close_db(conn)
        return {"status":"success", "msg": "Successfuly Read" , "res":res}
    except Exception as e :
        conn.rollback()    
        return {"status":"unsuccess", "msg": format(e) }
    finally:
        curr.close()
        close_db(conn)

@router.post("/question")
def question( id:int ):
    conn = get_db()
    curr= conn.cursor()   
    try:        
        query = "select * from Questions where qid = "+ str(id)
        curr.execute(query)    
        res = [dict((curr.description[i][0], value) \
                for i, value in enumerate(row)) for row in curr.fetchall()]
        
        query1 = "select `Oid`, `option`, `type` from Options where qid = "+ str(id)
        curr.execute(query1)    
        res1 = [dict((curr.description[i][0], value) \
                for i, value in enumerate(row)) for row in curr.fetchall()]
        res[0]['Options'] = res1

        curr.close()
        close_db(conn)
        return {"status":"success", "msg": "Successfuly Read" , "res":res}
    except Exception as e :   
        return {"status":"unsuccess", "msg": format(e) }
    finally:
        curr.close()
        close_db(conn)

@router.post("/attemptquestion")
def attemptquestion( req : AttemptQuestion ):
    conn = get_db()
    curr= conn.cursor()   
    try:   
        query = "select `Oid` from Answers where qid = "+ str(req.qid)
        curr.execute(query)    
        right_ans_id = curr.fetchone() 
        print(right_ans_id)
        if req.aid == right_ans_id:
            res = { "result":"true", "correctAns":"" }
            query = "insert into student_question( `St_id` , `qid` ) values("+ str(req.sid) + "," + str(req.qid) +")"
            # print("query",query)
            curr.execute(query)
            conn.commit()
        else:
            res = { "result":"false", "correctAns":"" }
        curr.close()
        close_db(conn)
        return {"status":"success", "msg": "Successfuly Read" , "res":res}
    except Exception as e :   
        return {"status":"unsuccess", "msg": format(e) }
    finally:
        curr.close()
        close_db(conn)

@router.post("/submitquiz")
def submitquiz( req : SubmitQuiz ):
    conn = get_db()
    curr= conn.cursor()   
    try:        
        n_corr_low = 0
        n_wron_low = 0
        n_unat_low = 0
        n_corr_mod = 0
        n_wron_mod = 0
        n_unat_mod = 0
        n_corr_hig = 0
        n_wron_hig = 0
        n_unat_hig = 0
        # date_time = str(datetime.now())

        query = "insert into Attempts( `St_id` , `Quiz_id` ) values("+ str(req.st_id) + "," + str(req.quizid) +")"
        curr.execute(query)
        curr.execute('SELECT LAST_INSERT_ID()')
        at_id = curr.fetchone()[0]
        
        records_to_insert = []
        for question in req.questions:
            flag = "Unattempted"
            query = "select `Oid` from Answers where qid = "+ str(question.qid)
            curr.execute(query)    
            right_ans_id = curr.fetchone() 
            # print('right_ans_id',right_ans_id , question.aid)
            if right_ans_id and question.aid :
                if question.aid[0] == right_ans_id[0] : #rightly answered
                    flag = "Right"
                    if question.diff_lvl == '1':
                        n_corr_low += 1
                    elif question.diff_lvl == '2':
                        n_corr_mod += 1
                    elif question.diff_lvl == '3':
                        n_corr_hig += 1
                    print('right')             
                elif question.aid[0] != right_ans_id[0] : #wrongly answered
                    flag = "Wrong"
                    if question.diff_lvl == '1':
                        n_wron_low += 1
                    elif question.diff_lvl == '2':
                        n_wron_mod += 1
                    elif question.diff_lvl == '3':
                        n_wron_hig += 1
                    print('wrong')
            else:
                print('Unattempted')
                if question.diff_lvl == '1':
                    n_unat_low += 1
                elif question.diff_lvl == '2':
                    n_unat_mod += 1
                elif question.diff_lvl == '3':
                    n_unat_hig += 1
            print(question)
            records_to_insert.append(( at_id , question.qid , question.time , flag ))
        score = (( n_corr_low + n_corr_mod + n_corr_hig ) / len(req.questions)) * 100
        print("score ",score)
        print( n_corr_low , n_corr_mod , n_corr_hig , n_wron_low , n_wron_mod , n_wron_hig , n_unat_low , n_unat_mod , n_unat_hig )
        
        mySql_insert_query = """INSERT INTO Timings (Aid, qid, time_taken , status) 
                           VALUES (%s, %s, %s, %s) """
        curr.executemany(mySql_insert_query, records_to_insert)

        query = """
                Update  Attempts a SET 
                a.score = %s , 
                a.n_corr_low = %s , 
                a.n_wron_low = %s ,
                a.n_unat_low = %s ,
                a.n_corr_mod = %s ,
                a.n_wron_mod = %s ,
                a.n_unat_mod = %s ,
                a.n_corr_hig = %s ,
                a.n_wron_hig = %s ,
                a.n_unat_hig = %s 
                where a.Aid = %s  
                """
        curr.execute(query , (score,n_corr_low,n_wron_low,n_unat_low,n_corr_mod,n_wron_mod,n_unat_mod,n_corr_hig,n_wron_hig,n_unat_hig, at_id) )

        # res = req    
        conn.commit()    
        return {"status":"success", "msg": "Successfuly Quiz Submitted" , "res" : at_id }
    except Exception as e :   
        return {"status":"unsuccess", "msg": format(e) }
    finally:
        curr.close()
        close_db(conn)

@router.post("/attemptedquizs")
def attemptedquizs( sid : int ):
    conn = get_db()
    curr= conn.cursor()   
    try: 
        query = "select a.Aid , a.Quiz_id, a.score, a.date_time from Attempts a where St_id = " + str(sid)
        curr.execute(query)
        res = [dict((curr.description[i][0], value) \
                for i, value in enumerate(row)) for row in curr.fetchall()]
        
        return {"status":"success", "msg": "Successfuly read Submitted Quizzes" , "res" : res }
    except Exception as e :   
        return {"status":"unsuccess", "msg": format(e) }
    finally:
        curr.close()
        close_db(conn)

@router.post("/showresult")
def showresult( aid : int ):
    conn = get_db()
    curr= conn.cursor()   
    try: 
        query = "select * from Attempts where Aid = " + str(aid)
        curr.execute(query)
        res = [dict((curr.description[i][0], value) \
                for i, value in enumerate(row)) for row in curr.fetchall()]
        
        query2 = "select `qid` , `time_taken` , `status` from Timings where Aid = " + str(aid)
        curr.execute(query2)
        res2 = [dict((curr.description[i][0], value) \
                for i, value in enumerate(row)) for row in curr.fetchall()]
        
        for quest in res2:
            quest["deatils"] = (question(quest['qid']))
            query = "select Oid from Answers where qid = " + str(quest['qid'])
            curr.execute(query)
            x = curr.fetchone()
            if x :
                quest["ans"] = x[0]
            else:
                quest["ans"] = None

        res[0]["questions"]=res2
        
        return {"status":"success", "msg": "Successfuly read Submitted Quizzes" , "res" : res }
    except Exception as e :   
        return {"status":"unsuccess", "msg": format(e) }
    finally:
        curr.close()
        close_db(conn)
