import sqlite3
from sqlite3 import Error

def conecta(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)

    except Error as e:
        print(e)
    finally:
        if conn is None:
            conn.close()
            print("Conexão Fechada")

if __name__ == '__main__':
    conecta('B:/lojapoo.sqlite3')