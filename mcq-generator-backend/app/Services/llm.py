# app/services/llm.py
import os
from openai import OpenAI
from dotenv import load_dotenv
from app.utils.chunk_text import chunk_text

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_mcqs(text: str, num_questions: int = 5):
    """
    Generate MCQs from text using chunking for better coverage.
    """
    # Split text into chunks (buffers)
    buffers = chunk_text(text, chunk_size=1000, overlap=150)

    all_mcqs = []

    for i, buffer in enumerate(buffers):
        prompt = f"""
        Generate {num_questions} multiple choice questions (MCQs) based on the following text:

        {buffer}

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
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        try:
            mcqs = response.choices[0].message.content
            all_mcqs.append(mcqs)
        except Exception as e:
            print(f"Error parsing LLM response for chunk {i}: {e}")

    return all_mcqs
