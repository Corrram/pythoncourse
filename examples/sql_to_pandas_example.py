import pandas as pd
import sqlite3

def main():
    conn = sqlite3.connect("../../music.db")
    query = "SELECT * FROM tracks;"
    tracks = pd.read_sql_query(query, conn)
    albums = pd.read_sql_query("SELECT * FROM albums;", conn)
    artists = pd.read_sql_query("SELECT * FROM artists;", conn)
    conn.close()

if __name__ == "__main__":
    main()