import sqlite3
conn = sqlite3.connect('lojapoo.sqlite3')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS produto(
id_produto INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
nome_produto TEXT,
preco_produto TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS cliente(
id_cliente INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
nome_cliente TEXT,
foto_cliente TEXT,
cpf_cliente TEXT,
id_produto INTEGER,
FOREIGN KEY (id_produto) REFERENCES produto(id_produto))

''')