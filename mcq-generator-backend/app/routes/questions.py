# app/routes/questions.py
from fastapi import APIRouter, HTTPException
from app.database import db
from app.Services.llm import generate_mcqs
from bson import ObjectId
import json

router = APIRouter()

@router.post("/generate-questions/{book_id}")
async def generate_questions(book_id: str, num_questions: int = 5):
    book = await db.books.find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Call LLM
    raw_output = await generate_mcqs(book["text"], num_questions=num_questions)

    try:
        questions = json.loads(raw_output)  # Expect valid JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing LLM response: {str(e)}")

    # Save to DB
    for q in questions:
        q["book_id"] = book_id
        await db.questions.insert_one(q)

    return {"msg": "Questions generated", "count": len(questions), "preview": questions[:2]}
