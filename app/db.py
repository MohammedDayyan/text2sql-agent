import sqlite3
import pandas as pd

db_path = 'database/data.db'

def execute_query(sql_query: str):
    
    try:
        for w in ['DROP','DELETE','UPDATE','INSERT','ALTER']:
            if w in sql_query:
                 raise Exception('Only SQL queries allowed.')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        return str(e)

def redeem_query(sql_query: str,db_path: str):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(sql_query,conn)
    conn.close()
    return df

def get_tables(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
                   SELECT name from sqlite_master where type='table';
                   """)
    
    tables = [t[0] for t in cursor.fetchall()]
    conn.close()
    
    return tables 

def get_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table';
    """)

    tables = cursor.fetchall()

    schema = ""

    for table in tables:
        t = table[0]
        cursor.execute(f"PRAGMA table_info({t})")
        cols = cursor.fetchall()
        schema += f"\nTable: {t}\n"
        for col in cols:
            schema += f"{col[1]} ({col[2]})\n"

    conn.close()
    return schema

    
    