from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict
from uuid import uuid4

app = FastAPI()


class Student(BaseModel):
    name: str = Field(..., example="Renuka")
    age: int = Field(..., gt=0, example=23)
    course: str = Field(..., example="Computer Science")


class StudentResponse(Student):
    id: str


students_db: Dict[str, Student] = {}

@app.post("/students", response_model=StudentResponse)
def add_student(student: Student):
    student_id = str(uuid4())
    students_db[student_id] = student
    return StudentResponse(id=student_id, **student.dict())


@app.get("/students", response_model=Dict[str, Student])
def get_all_students():
    return students_db


@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: str):
    student = students_db[student_id]
    return StudentResponse(id=student_id, **student.dict())


@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: str):
    del students_db[student_id]
    return