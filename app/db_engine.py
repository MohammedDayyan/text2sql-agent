from sqlalchemy import create_engine
import pandas as pd

def create_db_engine(db_type, db_path=None, host=None, user=None, password=None, database=None):
    
    if db_type == "sqlite":
        connection_string = f"sqlite:///{db_path}"

    elif db_type == "mysql":
        connection_string = f"mysql+pymysql://{user}:{password}@{host}/{database}"

    elif db_type == "postgres":
        connection_string = f"postgresql://{user}:{password}@{host}/{database}"

    else:
        raise ValueError("Unsupported DB type")

    return create_engine(connection_string)


def execute(engine, sql):
    return pd.read_sql(sql, engine)