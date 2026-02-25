from groq import Groq
import streamlit as st

client = Groq(api_key=st.secrets('GROQ_API_KEY'))

def explain_result(question, result):

    prompt = f"""
User asked:
{question}

SQL result:
{result}

Give business insight in 2 lines.
"""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{'role':'user','content':prompt}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()

