import pandas as pd
import sqlite3


def main():
    conn = sqlite3.connect("../music.db")
    query = "SELECT * FROM tracks;"
    _tracks = pd.read_sql_query(query, conn)
    _albums = pd.read_sql_query("SELECT * FROM albums;", conn)
    _artists = pd.read_sql_query("SELECT * FROM artists;", conn)
    conn.close()


if __name__ == "__main__":
    main()
