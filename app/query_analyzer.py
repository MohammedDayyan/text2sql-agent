from sqlalchemy import text

def get_explain_plan(engine, sql, db_type):
    try:
        if db_type == "sqlite":
            explain_sql = f"EXPLAIN QUERY PLAN {sql}"
        elif db_type == "mysql":
            explain_sql = f"EXPLAIN {sql}"
        elif db_type == "postgres":
            explain_sql = f"EXPLAIN {sql}"
        else:
            return "Unsupported DB type"

        with engine.connect() as conn:
            result = conn.execute(text(explain_sql))
            rows = result.fetchall()

        return rows

    except Exception as e:
        return f"Explain failed: {str(e)}"
    
def detect_heavy_query(plan_rows):
    warning_keywords = ["SCAN", "ALL", "SEQUENTIAL"]

    for row in plan_rows:
        row_str = str(row).upper()
        for keyword in warning_keywords:
            if keyword in row_str:
                return True

    return False