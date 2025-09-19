# app/routes/books.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.database import db
from PyPDF2 import PdfReader
import gridfs

router = APIRouter()

@router.post("/upload")
async def upload_book(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported for now.")

    # Save PDF file temporarily
    contents = await file.read()

    # Extract text from PDF
    try:
        reader = PdfReader(file.file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")

    # Store in Mongo
    book_doc = {
        "title": file.filename,
        "text": text,
    }
    result = await db.books.insert_one(book_doc)

    return {
        "msg": "Book uploaded successfully",
        "book_id": str(result.inserted_id),
        "text_preview": text[:500]  # first 500 chars only
    }



