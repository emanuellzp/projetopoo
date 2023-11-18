import sqlite3
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6 import uic

# Fábio Emanuell Abreu Cardoso e Nicolas Heitor Feitosa Costa
# POO - Implementação Sitema de Vendas de Produtos.

# Inserindo a classe ...
class Cliente_main(QWidget):
    def __init__(self):
        super().__init__()
        self.ui =uic.loadUi('cliente_form.ui', self)

        self.bt_inserir.clicked.connect(self.inserir_cliente)
        self.bt_buscar.clicked.connect(self.buscar)
        self.bt_editar.clicked.connect(self.editar)
        self.bt_excluir.clicked.connect(self.excluir)
        self.bt_foto.clicked.connect(self.inserir_foto)
        self.selecionar_produtos()
        self.add_foto = None
        self.show()

# Inserindo o cliente ...
    def inserir_cliente(self):
        try:
            nome = self.lineEdit_nome.text()
            cpf = self.lineEdit_cpf.text()
            produto = self.cb_produto.currentText()

            if not nome or not cpf or not produto:
                self.label_infos.setText("ERRO! ⚠️ Preencha todos os componentes.")
            else:
                conn = sqlite3.connect('lojapoo.sqlite3')
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO cliente (nome_cliente, cpf_cliente, foto_cliente, id_produto) VALUES (?, ?, ?, ?)",
                    (nome, cpf, self.add_foto, produto))
                conn.commit()
                self.ui.label_infos.setText(f"O cliente {nome} foi cadastrado! ✅")
                conn.close()
                self.limpar()
        except Exception as e:
            print(f"Ops! ⚠️Erro ao inserir cliente: {str(e)}")

# Criando a função de limpar a tela ...
    def limpar(self):
        self.ui.lineEdit_nome.setText("")
        self.ui.lineEdit_cpf.setText("")
        self.ui.lb_foto.setPixmap(QPixmap())
        self.ui.lineEdit_foto.setText("")
        self.ui.cb_produto.setCurrentIndex(0)

# Inserindo a busca de clientes ...
    def buscar(self):
        busca = self.ui.lineEdit_buscar.text()
        try:
            con = sqlite3.connect('lojapoo.sqlite3')
            cursor = con.cursor()
            if busca.isdigit():
                cursor.execute("SELECT * FROM cliente WHERE id_cliente == ?", (int(busca),))
            else:
                cursor.execute("SELECT * FROM cliente WHERE nome_cliente == ?", (busca,))
            b = cursor.fetchone()
            if b is not None:
                self.ui.lineEdit_nome.setText(b[1])
                self.ui.lineEdit_cpf.setText(b[3])
                self.ui.cb_produto.setCurrentText(b[4])
                add_foto = b[2]
                if add_foto:
                    pixmap = QPixmap(add_foto)
                    self.ui.lb_foto.setPixmap(pixmap)
                    self.ui.lb_foto.setScaledContents(True)
                else:
                    self.ui.lb_foto.setPixmap(QPixmap())
            else:
                self.ui.label_infos.setText("OPS! ⚠️Cliente não cadastrado!")
            con.close()
        except Exception as e:
            print(f"OPS! ⚠️ Erro ao buscar cliente: {str(e)}")

# Inserindo a função de modificar informações sobre os clientes ...

    def editar(self):
        cod = self.ui.lineEdit_buscar.text()
        nome = self.ui.lineEdit_nome.text()
        cpf = self.ui.lineEdit_cpf.text()
        produto = self.ui.cb_produto.currentText()
        foto = self.add_foto
        try:
            con = sqlite3.connect('lojapoo.sqlite3')
            cursor = con.cursor()
            cursor.execute("""
            UPDATE cliente SET
            nome_cliente = ?,
            cpf_cliente = ?,
            id_produto = ?,
            foto_cliente = ?
            WHERE 
            id_cliente = ?
            """, (nome, cpf, produto, foto, int(cod)))
            con.commit()
            con.close()
            self.ui.label_infos.setText("Atualização feita com sucesso! ✅")
            self.limpar()
        except Exception as e:
            self.ui.label_infos.setText(f"OPS! ⚠️ Erro ao atualizar cliente: {str(e)}")

# Inserindo a função de deletar ...

    def excluir(self):
        cod = self.ui.lineEdit_buscar.text()
        try:
            con = sqlite3.connect('lojapoo.sqlite3')
            cursor = con.cursor()
            cursor.execute("DELETE FROM cliente WHERE id_cliente = ?", (int(cod),))
            con.commit()
            con.close()
            self.ui.label_infos.setText("Sucesso! O cliente foi deletado. ✅")
            self.limpar()
        except Exception as e:
            self.ui.label_infos.setText(f"OPS!⚠️ Erro ao deletar o cliente: {str(e)}")


# Inserindo a função de inserir uma foto de identificação do cliente ...

    def inserir_foto(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar Foto", "", "Imagens (*.jpg *.png *.jpeg *.bmp);;Todos os Arquivos (*)")
            if file_path:
                pixmap = QPixmap(file_path)
                self.lb_foto.setPixmap(pixmap)
                self.lb_foto.setScaledContents(True)
                self.add_foto = file_path
        except Exception as e:
            print(f"OPS!⚠️ Erro ao selecionar foto: {str(e)}")

# Inserindo a função de selecionar produtos do produto main ...

    def selecionar_produtos(self):
        conn = sqlite3.connect('lojapoo.sqlite3')
        cursor = conn.cursor()
        cursor.execute("SELECT nome_produto FROM produto")
        produtos = [row[0] for row in cursor.fetchall()]
        conn.close()
        self.cb_produto.addItem("Selecione uma opção")
        self.cb_produto.addItems(produtos)

# Fim ...

if __name__=='__main__':
    janela = QApplication(sys.argv)
    app = Cliente_main()
    sys.exit(janela.exec())

