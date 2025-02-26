import duckdb
import time


def conectar_banco():
    """Conecta ao banco de dados DuckDB; cria o banco se não existir."""
    return duckdb.DuckDBPyConnection(database='duckdb.db', read_only=False)

def create_duckdb():
    con = duckdb.DuckDBPyConnection()
    con.execute("""
        SELECT OrderID, ProductID, SUM(Quantity) AS total_quantity
        FROM read_csv("data/merchandise-sales.csv", AUTO_DETECT=FALSE, sep=',', columns={'OrderID': 'INTEGER', 'ProductID': 'INTEGER', 'Quantity': 'INTEGER'})
        GROUP BY OrderID, ProductID
        ORDER BY total_quantity DESC
    """).fetchdf().show()

if __name__ == "__main__":
    import time
    start_time = time.time()
    conectar_banco()
    create_duckdb()
    took = time.time() - start_time
    print(f"Duckdb Took: {took:.2f} sec")