from fastapi import APIRouter
from sqlalchemy import false
from Quiz.database import *
from Quiz.dbmodels import *

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

@router.get("/classes" , tags=["class"])
def all_classes():
    conn = get_db()
    curr= conn.cursor()   
    curr.execute("select * from Classes")    
    res = [dict((curr.description[i][0], value) \
               for i, value in enumerate(row)) for row in curr.fetchall()]
    curr.close()
    close_db(conn)
    return {"status":"success", "msg": "Successfuly Read" , "res":res}

@router.post("/create_class", tags=["class"])
def create_class(cls:Class):
    conn = get_db()
    curr= conn.cursor()
    try:
        query = "insert into Classes(class) values('"+cls.name+"')"
        print("query",query)
        curr.execute(query)
        conn.commit()
        return {"status":"success", "msg": "Successfuly Created"}
    except:
        conn.rollback()    
        return {"status":"unsuccess", "msg": "some error"}
    finally:
        curr.close()
        close_db(conn)
    

@router.put("/update_class", tags=["class"])
def update_class(cls:Class):
    conn = get_db()
    curr= conn.cursor()
    try:
        query = "update Classes SET name = '"+ cls.name +"' where id = "+ str(cls.id) 
        print("query",query)
        curr.execute(query)
        conn.commit()
        return {"status":"success", "msg": "Successfuly Updated"}
    except:
        conn.rollback()    
        return {"status":"unsuccess", "msg": "some error"}
    finally:
        curr.close()
        close_db(conn)

@router.delete("/delete_class/{id}", tags=["class"])
def delete_class(id:int):
    conn = get_db()
    curr= conn.cursor()
    try:
        query = "delete from Classes where id = "+ str(id) 
        print("query",query)
        curr.execute(query)
        conn.commit()
        return {"status":"success", "msg": "Successfuly deleted"}
    except:
        conn.rollback()    
        return {"status":"unsuccess", "msg": "some error"}
    finally:
        curr.close()
        close_db(conn)
    
@router.get("/classes/subjects" , tags=["subject"])
def all_subjects():
    conn = get_db()
    curr= conn.cursor()   
    query = """ 
        SELECT c.Class, c.Cid, s.Subject, s.Sid
        FROM Subjects as s 
        LEFT JOIN Classes as c
        ON c.Cid = s.Cid order by c.Cid;
    """
    curr.execute(query)    
    res = [dict((curr.description[i][0], value) \
               for i, value in enumerate(row)) for row in curr.fetchall()]
    curr.close()
    close_db(conn)
    return {"status":"success", "msg": "Successfuly Read" , "res":res}

@router.get("/class/{id}/subjects" , tags=["subject"])
def all_subjects(id:int):
    conn = get_db()
    curr= conn.cursor()   
    query = "select * from Subjects where Cid = "+ str(id)
    curr.execute(query)    
    res = [dict((curr.description[i][0], value) \
               for i, value in enumerate(row)) for row in curr.fetchall()]
    curr.close()
    close_db(conn)
    return {"status":"success", "msg": "Successfuly Read" , "res":res}

@router.post("/create_subject", tags=["subject"])
def create_subject(sub:Subject):
    conn = get_db()
    curr= conn.cursor()
    try:
        query = "insert into Subjects(Cid , Subject) values("+ str(sub.class_id) + ",'" + sub.subject+"')"
        print("query",query)
        curr.execute(query)
        conn.commit()
        return {"status":"success", "msg": "Successfuly Created"}
    except Exception as e :
        conn.rollback()    
        return {"status":"unsuccess", "msg": format(e) }
    finally:
        curr.close()
        close_db(conn)
    

@router.put("/update_subject", tags=["subject"])
def update_subject(sub:Subject):
    conn = get_db()
    curr= conn.cursor()
    try:
        query = "update Subjects SET Cid ="+ sub.class_id +", subject = '"+ sub.subject +"' where Sid = "+ str(sub.id) 
        print("query",query)
        curr.execute(query)
        conn.commit()
        return {"status":"success", "msg": "Successfuly Updated"}
    except:
        conn.rollback()    
        return {"status":"unsuccess", "msg": "some error"}
    finally:
        curr.close()
        close_db(conn)
    

@router.delete("/delete_subject/{id}", tags=["subject"])
def delete_subject(id:int):
    conn = get_db()
    curr= conn.cursor()
    try:
        query = "delete from Subjects where Sid = "+ str(id) 
        print("query",query)
        curr.execute(query)
        conn.commit()
        return {"status":"success", "msg": "Successfuly deleted"}
    except:
        conn.rollback()    
        return {"status":"unsuccess", "msg": "some error"}
    finally:
        curr.close()
        close_db(conn)
    
@router.get("/classes/subject/chapters", tags=["chapter"])
def all_chapters():
    conn = get_db()
    curr= conn.cursor()   
    query = """select d.*, cp.Chapter , cp.CHid
            from (select c.Class, c.Cid , s.Subject, s.sid 
                from Classes c inner join Subjects s on c.Cid = s.Cid) d 
                inner join Chapters cp on cp.Sid = d.Sid  ;
            """
    curr.execute(query)    
   
    res = [dict((curr.description[i][0], value) \
               for i, value in enumerate(row)) for row in curr.fetchall()]
    xyz = []
    for row in res:
        if len(xyz) == 0 :
            xyz.append({"Class":row["Class"] , 
                        "Cid":row["Cid"] , 
                        "Subject":row["Subject"],
                        "sid":row["sid"],
                        "chapters":[ {"name":row["Chapter"],
                                    "id":row["CHid"]} ]})
        else:
            for sub in xyz:
                if row["sid"] == sub["sid"] and {"name":row["Chapter"] , "id":row["CHid"]} not in sub["chapters"] :
                    sub["chapters"].append({"name":row["Chapter"] , "id":row["CHid"]})
                elif row["sid"] != sub["sid"] :
                    xyz.append({"Class":row["Class"] , 
                        "Cid":row["Cid"] , 
                        "Subject":row["Subject"],
                        "sid":row["sid"],
                        "chapters":[ {"name":row["Chapter"],
                                    "id":row["CHid"]} ]})

    curr.close()
    close_db(conn)
    return {"status":"success", "msg": "Successfuly Read" , "res":xyz}


@router.get("/subject/{id}/chapters", tags=["chapter"])
def all_chapters(id:int):
    conn = get_db()
    curr= conn.cursor()   
    query = "select * from Chapters where Sid = "+ str(id)
    curr.execute(query)    
    res = [dict((curr.description[i][0], value) \
               for i, value in enumerate(row)) for row in curr.fetchall()]
    curr.close()
    close_db(conn)
    return {"status":"success", "msg": "Successfuly Read" , "res":res}


@router.post("/create_chapter", tags=["chapter"])
def create_chapter(ch:Chapter):
    conn = get_db()
    curr= conn.cursor()
    try:
        query = "insert into Chapters(Sid , Chapter) values("+ str(ch.sub_id) + ",'" + ch.chapter+"')"
        print("query",query)
        curr.execute(query)
        conn.commit()
        return {"status":"success", "msg": "Successfuly Created"}
    except Exception as e :
        conn.rollback()    
        return {"status":"unsuccess", "msg": format(e) }
    finally:
        curr.close()
        close_db(conn)

@router.put("/update_chapter", tags=["chapter"])
def update_chapter(ch:Chapter):
    conn = get_db()
    curr= conn.cursor()
    try:
        query = "update Chapters SET Sid ="+ ch.sub_id +", Chapter = '"+ ch.chapter +"' where CHid = "+ str(ch.id) 
        print("query",query)
        curr.execute(query)
        conn.commit()
        return {"status":"success", "msg": "Successfuly Updated"}
    except:
        conn.rollback()    
        return {"status":"unsuccess", "msg": "some error"}
    finally:
        curr.close()
        close_db(conn)

@router.delete("/delete_chapter/{id}", tags=["chapter"])
def delete_chapter(id:int):
    conn = get_db()
    curr= conn.cursor()
    try:
        query = "delete from Chapters where CHid = "+ str(id) 
        print("query",query)
        curr.execute(query)
        conn.commit()
        return {"status":"success", "msg": "Successfuly deleted"}
    except:
        conn.rollback()    
        return {"status":"unsuccess", "msg": "some error"}
    finally:
        curr.close()
        close_db(conn)

@router.get("/chapter/{id}/tags", tags=["tag"])
def all_tags(id:int):
    conn = get_db()
    curr= conn.cursor()   
    query = "select * from Tags where CHid = "+ str(id)
    curr.execute(query)    
    res = [dict((curr.description[i][0], value) \
               for i, value in enumerate(row)) for row in curr.fetchall()]
    curr.close()
    close_db(conn)
    return {"status":"success", "msg": "Successfuly Read" , "res":res}

@router.post("/create_tag", tags=["tag"])
def create_tag(tag:Tag):
    conn = get_db()
    curr= conn.cursor()
    try:
        query = "insert into Tags(CHid , tag) values("+ str(tag.chap_id) + ",'" + tag.tag+"')"
        print("query",query)
        curr.execute(query)
        conn.commit()
        return {"status":"success", "msg": "Successfuly Created"}
    except Exception as e :
        conn.rollback()    
        return {"status":"unsuccess", "msg": format(e) }
    finally:
        curr.close()
        close_db(conn)

@router.put("/update_tag", tags=["tag"])
def update_tag(tag:Tag):
    conn = get_db()
    curr= conn.cursor()
    try:
        query = "update Tags SET CHid ="+ tag.chap_id +", tag = '"+ tag.tag +"' where tag_id = "+ str(tag.id) 
        print("query",query)
        curr.execute(query)
        conn.commit()
        return {"status":"success", "msg": "Successfuly Updated"}
    except:
        conn.rollback()    
        return {"status":"unsuccess", "msg": "some error"}
    finally:
        curr.close()
        close_db(conn)

@router.delete("/delete_tag/{id}", tags=["tag"])
def delete_tag(id:int):
    conn = get_db()
    curr= conn.cursor()
    try:
        query = "delete from Tags where tag_id = "+ str(id) 
        print("query",query)
        curr.execute(query)
        conn.commit()
        return {"status":"success", "msg": "Successfuly deleted"}
    except:
        conn.rollback()    
        return {"status":"unsuccess", "msg": "some error"}
    finally:
        curr.close()
        close_db(conn)

@router.post("/create_question", tags=["question"])
def create_question(quests:Questions):
    conn = get_db()
    curr= conn.cursor()
    try:
        for i in range( len(quests.questions)):
            query = "insert into Questions(CHid , question, dificulty_lvl) values("+ str(quests.chap_id) + ",'" + quests.questions[i].question + "','" + quests.questions[i].diff_lvl +"')"
            print("query",query)
            curr.execute(query)

            for j in range( len(quests.questions[i].options)):
                query1 = "insert into Options( `qid` , `option` ) values ((SELECT `qid` from Questions WHERE CHid = "+ str(quests.chap_id) +" and question = '"+ quests.questions[i].question +"' ) , '"+ str(quests.questions[i].options[j].value) +"')"
                print("query1",query1 )
                curr.execute(query1)

                if quests.questions[i].options[j].isAns:
                    query2 = "insert into Answers( `qid` , `Oid` ) values ((SELECT `qid` from Questions WHERE CHid = "+ str(quests.chap_id) +" and question = '"+ quests.questions[i].question +"' ) , (SELECT `Oid` from Options WHERE `qid` = (SELECT `qid` from Questions WHERE CHid = "+ str(quests.chap_id) +" and question = '"+ quests.questions[i].question +"' ) and `option` = '"+ quests.questions[i].options[j].value +"' ))"
                    print("query2",query2)
                    curr.execute(query2)
    
        conn.commit()
        return {"status":"success", "msg": "Successfuly Qustions Created" , "res": quests}
    except Exception as e :
        conn.rollback()    
        return {"status":"unsuccess", "msg": format(e) }
    finally:
        curr.close()
        close_db(conn)

@router.delete("/delete_question/{id}", tags=["question"])
def delete_question(id:int):
    conn = get_db()
    curr= conn.cursor()
    try:
        query = "delete from Questions where qid = "+ str(id) 
        print("query",query)
        curr.execute(query)
        conn.commit()
        return {"status":"success", "msg": "Successfuly deleted"}
    except Exception as e:
        conn.rollback()    
        return {"status":"unsuccess", "msg": e}
    finally:
        curr.close()
        close_db(conn)