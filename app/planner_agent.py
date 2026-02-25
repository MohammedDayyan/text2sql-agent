from app.agent import generate_sql

def plan_query(question, schema):
    planning_prompt = f"""
You are a database planning agent.

User question:
{question}

Schema:
{schema}

Break the problem into logical steps.
For each step, describe what needs to be computed.

Return in numbered format.
"""

    plan = generate_sql(planning_prompt)
    return plan

def generate_sql_from_plan(question, schema):
    plan = plan_query(question, schema)

    final_prompt = f"""
User question:
{question}

Execution Plan:
{plan}

Schema:
{schema}

Now generate the final optimized SQL query.
Return only SQL.
"""

    sql = generate_sql(final_prompt)
    return plan, sql