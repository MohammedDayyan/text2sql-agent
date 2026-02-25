from app.agent import generate_sql

def validate_sql(question, sql, schema):
    validation_prompt = f"""
You are a strict SQL validator.

Schema:
{schema}

User question:
{question}

Generated SQL:
{sql}

Check for:
- Non-existent tables
- Non-existent columns
- Missing GROUP BY
- Dangerous operations (DROP, DELETE, UPDATE)
- Cartesian joins

If SQL is valid, return:
VALID

If invalid, return corrected SQL only.
"""

    result = generate_sql(validation_prompt)
    return result.strip()