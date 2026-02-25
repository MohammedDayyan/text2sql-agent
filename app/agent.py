from groq import Groq
from app.prompt_templates import SQL_PROMPT
import os
from dotenv import load_dotenv
from app.schema import TAB
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_sql(question: str):
    prompt = SQL_PROMPT.format(question=question,TAB=TAB)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()
