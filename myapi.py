from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()
students ={
    1:{
        "name":"John",
        "age":18,
        "year":"year 12",
    },
     
}

class Student(BaseModel):
    name:str
    age:int
    year:str

class updateStudent(BaseModel):
    name:str=None
    age:int=None
    year:str=None

@app.get("/")
def index():
    return  students[1]['name']

@app.get("/get-student/{student_id}")
def get_student(student_id:int = Path(..., description="the id of the student you want view")):
    return students[student_id]

@app.get("/get-by-name/{student_id}")
def get_student_by_name(student_id: int, name: Optional[str] = None):
    if student_id in students:
        student = students[student_id]
        if student["name"] == name:
            return {"Data": student}
        elif not name:
            return {"Data": student}
    
    return {"Data": "Not found"} 

@app.post("/create-student/{student_id}")
def create_student(student_id:int, student: Student):
    if student_id in students:
        return {"Error":"Student exist"}  
    students[student_id]=student
    #students[student_id]=student.dict()
    return {"Message": "Student created successfully"}

@app.delete("/delete-student/{student_id}")
def delete_student(student_id:int):
    if student_id in students:
        #deleted_student= students.pop(student_id)
        deleted_student=students[student_id]
        del students[student_id]
        return {"message": f"the student {deleted_student['name']} is deleted successfully"}
    return {"message": f"the student with the given id {student_id} doesn't exist"}

@app.put("/update-student/{student_id}")
def update_student(student_id: int, updated_info: updateStudent):
    if student_id not in students:
        return {"Error message": f"Student with the given student ID number {student_id} isn't found in the database"}
    students[student_id].update(updated_info.dict(exclude_unset=True))
    return {"message": f"the student with the given ID number {student_id} is successfully updated"}
        