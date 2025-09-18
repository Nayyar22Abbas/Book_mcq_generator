# app/services/llm.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_mcqs(text: str, num_questions: int = 5):
    prompt = f"""
    Generate {num_questions} multiple choice questions (MCQs) based on the following text:

    {text[:2000]}  # send only first 2000 chars to stay within token limits

    Format your output as JSON:
    [
        {{
            "question": "What is ...?",
            "options": ["A", "B", "C", "D"],
            "correct_answer": "A"
        }},
        ...
    ]
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # use GPT-4o-mini or GPT-4.1 if available
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content
