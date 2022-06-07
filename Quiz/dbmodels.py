from operator import contains
from token import OP
from typing import List, Optional
from pydantic import BaseModel , HttpUrl

class Class(BaseModel):
    id: Optional[int]
    name: str

class Subject(BaseModel):
    id: Optional[int]
    class_id: int
    subject: str

class Chapter(BaseModel):
    id: Optional[int]
    sub_id: int
    chapter: str

class Tag(BaseModel):
    id : Optional[int]
    chap_id : int
    tag : str

class Institute(BaseModel):
    id : Optional[int]
    email : str
    password : str
    phone : int

# class Question(BaseModel):
#     id : Optional[int]
#     in_id: Optional[int]
#     chap_id : int
#     question : str
#     q_type : str 
#     diff_lvl: str
#     contains_img : Optional[int] = 0

class Image(BaseModel):
    url: HttpUrl
    name: str

class Option(BaseModel):
    id : int
    type : str = None
    value : str
    fileImg : str = None
    isAns : bool = False

class Question(BaseModel):   
    question : str      
    q_type : str 
    diff_lvl: str
    ans_id : list[int]
    options : list[Option]
    has_img : bool = False
    images : list[Image] = None
    
class Questions(BaseModel):
    classid : int
    sub_id : int
    chap_id : int
    questions : list[Question]

class Quest_tags(BaseModel):
    qid: Optional[int]
    tag_id : int

class Quest_imgs(BaseModel):
    qid : Optional[int]
    img_seq : int
    img_src : Optional[str]

class Options(BaseModel):
    id : Optional[int]
    qid : int
    option : str
    type : Optional[int]

class Answers(BaseModel):
    qid : int
    oid : int

class Student(BaseModel):
    id : Optional[int]
    in_id : Optional[int] = 0
    name : str
    email : str
    phone : int
    password : Optional[str] = "123"
    point : Optional[int] = 0
    score : Optional[int] = 0
    performance_lvl : Optional[str] 

class Problem(BaseModel):
    cid : Optional[int] = None
    sid: Optional[int] = None     
    CHid: Optional[int] = None
    dificulty_lvl : Optional[str] = None

class Quiz(BaseModel):
    sid: int
    cid : int
    subid : Optional[int]
    chid : Optional[int]

class StudQuizId(BaseModel):
    sid: int
    quiz_id : int
    
class AttemptQuestion(BaseModel):
    qid : int
    aid : list[int]
    time : Optional[int]
    sid : Optional[int] 
    q_type : Optional[str] 
    diff_lvl : Optional[str] 

class SubmitQuiz(BaseModel):
    st_id : int
    quizid : int
    questions : list[AttemptQuestion]