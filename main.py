from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from fastapi.responses import HTMLResponse

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool


class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]


def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_database)]


@app.get("/questions/{question_id}")
async def read_question(question_id: int, db: db_dependency):
    """SELECT * FROM questions WHERE id = {question_id} LIMIT 1"""
    result = (
        db.query(models.Questions).filter(models.Questions.id == question_id).first()
    )
    if not result:
        raise HTTPException(status_code=404, detail="Question not found!")
    return result


@app.get("/choices/{question_id}")
async def read_choices(question_id: int, db: db_dependency):
    """SELECT * FROM choices WHERE question_id = {question_id}"""
    result = (
        db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    )
    if not result:
        raise HTTPException(404, detail="Choices not found!")
    return result


@app.delete("/questions/{question_id}")
async def delete_question(question_id: int, db: db_dependency):
    """DELETE FROM questions WHERE id = {question_id}"""
    query_job = (
        db.query(models.Questions).where(models.Questions.id == question_id).first()
    )
    if query_job:
        db.delete(query_job)
        db.commit()
        return {"message": "deleted"}
    return {"message": "Question not found!"}


@app.get("/", response_class=HTMLResponse)
async def main(db: db_dependency):
    """SELECT * FROM questions ORDER BY RAND() //PostgreSQL specific"""
    result = db.query(models.Questions).order_by(func.random()).first()
    if not result:
        raise HTTPException(404, "No questions found")
    output = f"{result.question_text}\n"
    for number, choice in enumerate(result.choices):
        output += f"{number}. {choice.choice_text}\n"
    return output


@app.post("/questions/")
async def create_questions(question: QuestionBase, db: db_dependency):
    """INSERT INTO questions(id, question_text, choices) VALUES (1, foo, bar...);
    INSERT INTO choices(id, choice_text, is_correct, question_id) VALUES (1, foo, false, 1)
    """
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=db_question.id,
        )
        db.add(db_choice)
        db.commit()
