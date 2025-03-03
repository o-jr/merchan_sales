import db.duckdb as duckdb
import time


def create_duckdb():
    # Method 1: Using the read_csv function directly to create a DataFrame in duckdb
    con = duckdb.connect(database=':memory:', read_only=False) # Establish a connection - ':memory:' creates an in-memory database
    df = con.read_csv('data/merchandise-sales.csv', header=True) # Reads the CSV and returns it to the Dataframe
    print(df)       
    con.close()

if __name__ == "__main__":
    start_time = time.time()

    create_duckdb()

    took = time.time() - start_time
    print(f"Duckdb Tooks: {took:.2f} sec")

