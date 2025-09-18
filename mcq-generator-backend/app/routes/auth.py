# app/routes/auth.py
from fastapi import APIRouter, HTTPException
from app.database import db
from app.models import User

router = APIRouter()

@router.post("/register")
async def register(user: User):
    try:
        print("📌 Register request:", user.dict())  # Debug
        existing = await db.users.find_one({"username": user.username})
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")

        result = await db.users.insert_one(user.dict())
        print("✅ Inserted ID:", result.inserted_id)  # Debug
        return {"msg": "User registered successfully"}
    except Exception as e:
        print("❌ Error in /auth/register:", str(e))  # Debug
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")
