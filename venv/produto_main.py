import sqlite3
import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import uic
from produto_form import Ui_produto
from sqlite3 import Error as e

sys.path.append("C:\Scripts\poo2023-main\ venv")
class Produto_main(QWidget):
    def __init__(self):
        super().__init__()
        self.ui =uic.loadUi('produto_form.ui',self)
        self.ui.bt_inserir.clicked.connect(self.inserir_produto)
        self.ui.bt_buscar.clicked.connect(self.buscar)
        self.ui.bt_editar.clicked.connect(self.editar)
        self.ui.bt_excluir.clicked.connect(self.excluir)
        self.show()


    def inserir_produto(self):
        nome = self.ui.lineEdit_nome.text()
        preco = self.ui.lineEdit_preco.text()
        msg = "Produto cadastrado com sucesso:"
        try:
            con = sqlite3.connect('lojapoo.sqlite3')
            cursor = con.cursor()
            cursor.execute('''
            INSERT INTO produto(nome_produto, preco_produto)VALUES (?,?)''',
                           (nome,preco))
            con.commit()
            self.ui.label_msg.setText(msg+ " "+ nome)
            con.close()
            self.limpar()
        except e:
            self.ui.label_msg.setText(e)
    def limpar(self):
        self.ui.lineEdit_nome.setText("")
        self.ui.lineEdit_preco.setText("")


    def buscar(self):
        busca = self.ui.lineEdit_buscar.text()
        try:
            con = sqlite3.connect('lojapoo.sqlite3')
            cursor = con.cursor()
            cursor.execute('''
            SELECT * FROM produto WHERE id_produto = ?
            ''', (int(busca),))
            b= cursor.fetchone()
            if b is not None:
                self.ui.lineEdit_nome.setText(b[1])
                self.ui.lineEdit_preco.setText(b[2])
        except e:
            self.ui.label_msg.setText(e)


    def editar(self):
        cod = self.ui.lineEdit_buscar.text()
        nome = self.ui.lineEdit_nome.text()
        preco = self.ui.lineEdit_preco.text()
        try:
            con = sqlite3.connect('lojapoo.sqlite3')
            cursor = con.cursor()
            cursor.execute("""
            UPDATE produto SET
            nome_produto =?,
            preco_produto =?
            WHERE 
            id_produto ==?
            """, (nome, preco, int(cod)))
            con.commit()
            con.close()
        except e:
            self.ui.label_msg(e)


    def excluir(self):
        buscar = self.ui.lineEdit_buscar.text()
        nome = self.ui.lineEdit_nome.text()
        try:
            con = sqlite3.connect('lojapoo.sqlite3')
            cursor = con.cursor()
            cursor.execute('''DELETE FROM produto
            WHERE id_produto==?''',(buscar))
            con.commit()
            con.close()
            self.limpar()
            self.ui.label_msg.setText("Produto deletado!"+" "+nome)
        except e:
            self.ui.label_msg(e)

    def limpar(self):
        self.ui.lineEdit_nome.setText("")
        self.ui.lineEdit_preco.setText("")



if __name__=='__main__':
    janela = QApplication(sys.argv)
    app = Produto_main()
    sys.exit(janela.exec())

app = QApplication([])

produto_form = Ui_produto()

produto_form.show()

app.exec()