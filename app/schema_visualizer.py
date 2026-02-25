from sqlalchemy import inspect
import graphviz

def generate_er_diagram(engine):
    inspector = inspect(engine)
    dot = graphviz.Digraph()

    tables = inspector.get_table_names()

    for table in tables:
        columns = inspector.get_columns(table)
        col_names = [col["name"] for col in columns]

        label = f"{table}|" + "\\l".join(col_names) + "\\l"
        dot.node(table, label=label, shape="record")

        fks = inspector.get_foreign_keys(table)

        for fk in fks:
            referred_table = fk["referred_table"]
            dot.edge(table, referred_table)

    return dot