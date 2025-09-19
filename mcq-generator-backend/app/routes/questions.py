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

    # Call LLM → now returns a list of JSON strings
    raw_outputs = await generate_mcqs(book["text"], num_questions=num_questions)

    all_questions = []

    for i, raw in enumerate(raw_outputs):
        try:
            parsed = json.loads(raw)  # Expect each chunk to be a valid JSON array
            all_questions.extend(parsed)
        except Exception as e:
            print(f"⚠️ Error parsing chunk {i}: {e}")
            continue  # skip bad chunks

    if not all_questions:
        raise HTTPException(status_code=500, detail="No valid questions could be parsed from LLM output")

    # Save to DB
    for q in all_questions:
        q["book_id"] = book_id
        await db.questions.insert_one(q)

    return {
        "msg": "Questions generated",
        "count": len(all_questions),
        "preview": all_questions[:2]  # return just 2 for preview
    }
