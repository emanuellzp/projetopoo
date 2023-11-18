import sqlite3
from sqlite3 import Error as e
class Produto:
    def __init__(self, id,nome, desc, preco):
        self.id = id
        self.nome = nome
        self.desc = desc
        self.preco= preco

    def cad_produto(self):
        try:
            conn = sqlite3.connect('B:/loja.sqlite3')
            cursor = conn.cursor()
            self.nome = input('Digite o nome do produto: ')
            self.desc = input('Digite o descrição do produto: ')
            self.preco = input('Digite o preço do produto: ')

            cursor.execute("""INSERT INTO produto (nome,desc,preco) VALUES (?,?,?)
            """, (self.nome, self.desc, self.preco))
            conn.commit()
            conn.close()
        except e:
            print(e)


    def mostrar_produto(self):
        try:
            conn = sqlite3.connect('B:/loja.sqlite3')
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM produto""")
            for produto in cursor:
                print(produto)
        except e:
            print(e)


    def mostrar_id(self):
        try:
            conn = sqlite3.connect('B:/loja.sqlite3')
            cursor = conn.cursor()
            self.id =input('Pesquisa o Id: ')
            cursor.execute("""SELECT * FROM produto WHERE id=?""",(self.id))
            print(cursor.fetchone())
        except e:
            print(e)


    def mostrar_nome(self):
        try:
            conn = sqlite3.connect('B:/loja.sqlite3')
            cursor = conn.cursor()
            self.nome =input('Pesquisa o Nome:')
            cursor.execute("""SELECT * FROM produto WHERE nome=?""",(self.nome,))
            print(cursor.fetchall())
            conn.commit()
            conn.close()
        except e:
            print(e)


    def deletar_id(self):
        try:
            conn = sqlite3.connect('B:/loja.sqlite3')
            cursor = conn.cursor()
            self.id =input('Delete o Produto com Id: ')
            cursor.execute("""DELETE FROM produto WHERE id=?""",(self.id))
            conn.commit()
            conn.close()
        except e:
            print(e)


    def editar_id(self):
        try:
            conn = sqlite3.connect('B:/loja.sqlite3')
            cursor = conn.cursor()
            self.id =input('Editar o Produto com Id: ')
            self.nome = input("Novo nome:")
            self.desc = input("Nova descrição")
            self.preco = input("Novo preco")
            cursor.execute("""UPDATE produto
            SET nome =?,desc =?,preco=?
            WHERE id=?""",(self.nome,self.desc, self.preco,self.id))
            conn.commit()
            conn.close()
        except e:
            print(e)

