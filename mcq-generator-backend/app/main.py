from fastapi import FastAPI
from app.routes import auth, books, questions

app = FastAPI()

# Mount routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(questions.router, prefix="/questions", tags=["questions"])
