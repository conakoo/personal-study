import os

import sqlalchemy

import scrape

functions = [
    scrape.league_table,
    scrape.top_scorers,
]

CONN_STRING = os.getenv("CONN_STRING")

db = sqlalchemy.create_engine(CONN_STRING)
conn = db.connect()
for func in functions:
    function_name = func.__name__
    df = func()  # Call the function to get the DataFrame
    df.to_sql(function_name, con=conn, if_exists="replace", index=False)
    print(f"Pushed data for {function_name}")

# Close the database connection
conn.close()
