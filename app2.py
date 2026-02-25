import streamlit as st
import pandas as pd
import tempfile

from app.agent import generate_sql
from app.sql_validator import validate_sql
from app.db_engine import create_db_engine, execute
from app.schema_visualizer import generate_er_diagram
from app.analyst import explain_result
from app.planner_agent import generate_sql_from_plan
from app.query_analyzer import get_explain_plan, detect_heavy_query

from cache.caching import get_cached_sql, store_sql
from cache.semantic_cache import get_semantic_sql, store_semantic_sql

from sqlalchemy import inspect


# ---------------- CONFIG ----------------

st.set_page_config(page_title="AI SQL Analyst", layout="wide")
st.title("AI SQL Analyst Dashboard")
st.caption("Natural language → Planning → Validation → Cost Analysis → Execution → Insights")


# ---------------- SESSION ----------------

if "history" not in st.session_state:
    st.session_state.history = []


# ---------------- DATABASE SELECTION ----------------

st.sidebar.header("Database Connection")

db_type = st.sidebar.selectbox(
    "Select Database Type",
    ["sqlite", "mysql", "postgres"]
)

engine = None
db_identifier = None


# -------- SQLITE --------

if db_type == "sqlite":
    uploaded_file = st.sidebar.file_uploader(
        "Upload SQLite .db file",
        type=["db"]
    )

    if uploaded_file:
        temp_db = tempfile.NamedTemporaryFile(delete=False)
        temp_db.write(uploaded_file.read())
        db_path = temp_db.name

        engine = create_db_engine("sqlite", db_path=db_path)
        db_identifier = db_path


# -------- MYSQL --------

elif db_type == "mysql":
    host = st.sidebar.text_input("Host")
    user = st.sidebar.text_input("User")
    password = st.sidebar.text_input("Password", type="password")
    database = st.sidebar.text_input("Database")

    if host and user and password and database:
        engine = create_db_engine(
            "mysql",
            host=host,
            user=user,
            password=password,
            database=database
        )
        db_identifier = f"{host}_{database}"


# -------- POSTGRES --------

elif db_type == "postgres":
    host = st.sidebar.text_input("Host")
    user = st.sidebar.text_input("User")
    password = st.sidebar.text_input("Password", type="password")
    database = st.sidebar.text_input("Database")

    if host and user and password and database:
        engine = create_db_engine(
            "postgres",
            host=host,
            user=user,
            password=password,
            database=database
        )
        db_identifier = f"{host}_{database}"


# ---------------- STOP IF NO ENGINE ----------------

if not engine:
    st.warning("Please connect to a database.")
    st.stop()


# ---------------- SCHEMA + TABLES ----------------

inspector = inspect(engine)
tables = inspector.get_table_names()

st.sidebar.subheader("Tables")
selected_table = st.sidebar.selectbox("Preview Table", tables)

if selected_table:
    preview_df = execute(engine, f"SELECT * FROM {selected_table} LIMIT 100")
    st.subheader(f"Preview: {selected_table}")
    st.dataframe(preview_df, use_container_width=True)


# ---------------- ER DIAGRAM ----------------

if st.sidebar.button("Show ER Diagram"):
    er = generate_er_diagram(engine)
    st.graphviz_chart(er)


# ---------------- BUILD SCHEMA STRING ----------------

schema = ""
for table in tables:
    columns = inspector.get_columns(table)
    schema += f"\nTable: {table}\n"
    for col in columns:
        schema += f"{col['name']} ({str(col['type'])})\n"


# ---------------- QUESTION INPUT ----------------

st.markdown("---")

question = st.text_input("Ask a question about your data")

use_planner = st.checkbox("Use Multi-Step Planner Agent")
show_explain = st.checkbox("Show Query Execution Plan")


# ---------------- QUERY PIPELINE ----------------

if st.button("Run Query") and question:

    cache_key = question + str(db_identifier)

    # -------- EXACT CACHE --------
    cached_sql = get_cached_sql(cache_key)

    if cached_sql:
        st.info("Using exact cached SQL")
        sql = cached_sql

    else:
        # -------- SEMANTIC CACHE --------
        semantic_sql = get_semantic_sql(cache_key)

        if semantic_sql:
            st.info("Using semantic cached SQL")
            sql = semantic_sql

        else:
            # -------- PLANNER (OPTIONAL) --------
            if use_planner:
                plan, sql = generate_sql_from_plan(question, schema)

                st.subheader("Multi-Step Plan")
                st.write(plan)
            else:
                sql = generate_sql(
                    question + f"\nSCHEMA:\n{schema}"
                )

            # -------- VALIDATION --------
            validation_result = validate_sql(question, sql, schema)

            if validation_result != "VALID":
                st.warning("SQL corrected by validator")
                sql = validation_result

            # -------- STORE CACHE --------
            store_sql(cache_key, sql)
            store_semantic_sql(cache_key, sql)

    # -------- DISPLAY SQL --------
    st.subheader("Generated SQL")
    st.code(sql, language="sql")

    # -------- EXPLAIN PLAN (COST ANALYZER) --------
    if show_explain:
        plan_rows = get_explain_plan(engine, sql, db_type)

        st.subheader("Execution Plan")
        st.write(plan_rows)

        if isinstance(plan_rows, list) and detect_heavy_query(plan_rows):
            st.warning("⚠️ Potential Full Table Scan Detected — Query May Be Expensive for huge databases.")

    # -------- EXECUTE --------
    try:
        result = execute(engine, sql)

        if isinstance(result, pd.DataFrame):
            st.subheader("Query Result")
            st.dataframe(result, use_container_width=True)

            # -------- AUTO VISUALIZATION --------
            numeric_cols = result.select_dtypes(include=["number"]).columns

            if len(numeric_cols) >= 1:
                st.subheader("Auto Chart")
                st.bar_chart(result[numeric_cols])

        else:
            st.write(result)

        # -------- ANALYST EXPLANATION --------
        review = explain_result(question, result)

        st.subheader("AI Analyst Explanation")
        st.write(review)

        # -------- HISTORY --------
        st.session_state.history.append({
            "question": question,
            "sql": sql,
            "rows": len(result) if isinstance(result, pd.DataFrame) else "NA"
        })

    except Exception as e:
        st.error(f"Query failed: {str(e)}")


# ---------------- SIDEBAR HISTORY ----------------

st.sidebar.subheader("Query History")

for item in reversed(st.session_state.history[-10:]):
    st.sidebar.markdown(f"**Q:** {item['question']}")
    st.sidebar.caption(f"Rows: {item['rows']}")
    st.sidebar.code(item["sql"], language="sql")