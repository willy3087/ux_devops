from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox, QDialog, QLineEdit, QLabel, QFormLayout
import csv
import os

class EditarCadastroDialog(QDialog):
    def __init__(self, dados_linha, parent=None):
        super().__init__(parent)
        self.dados_linha = dados_linha
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Editar Cadastro")
        layout = QFormLayout()

        self.inputs = []
        for i, valor in enumerate(self.dados_linha):
            if i < len(self.dados_linha) - 1:  # Ignora a coluna do botão
                label = QLabel(f"Campo {i+1}:")
                line_edit = QLineEdit(valor)
                self.inputs.append(line_edit)
                layout.addRow(label, line_edit)

        self.btn_salvar = QPushButton("Salvar")
        self.btn_salvar.clicked.connect(self.salvar)
        layout.addRow(self.btn_salvar)

        self.setLayout(layout)

    def salvar(self):
        novos_dados = [input.text() for input in self.inputs]
        self.accept()  # Fecha o diálogo
        self.parent().salvar_edicao(self.dados_linha[0], novos_dados)  # Chama o método de salvar do parent

class VisualizacaoTarefas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualização de Cadastros")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(6)  # Ajuste conforme o número de colunas no CSV
        self.table.setHorizontalHeaderLabels(["Título", "Descrição", "Prioridade", "Cliente", "Sprint", "Ações"])
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        self.carregar_dados()

    def carregar_dados(self):
        self.table.setRowCount(0)  # Limpa a tabela antes de carregar
        arquivo_csv = os.path.join('data', 'tarefas.csv')
        if not os.path.exists(arquivo_csv):
            QMessageBox.information(self, "Informação", "Arquivo de dados não encontrado.")
            return

        with open(arquivo_csv, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for rowIndex, row in enumerate(reader):
                self.table.insertRow(rowIndex)
                for columnIndex, item in enumerate(row):
                    if columnIndex < 5:  # As primeiras 5 colunas são dados
                        self.table.setItem(rowIndex, columnIndex, QTableWidgetItem(item))
                # Adiciona os botões de edição e exclusão na última coluna
                btn_editar = QPushButton('Editar')
                btn_editar.clicked.connect(lambda ch, row=rowIndex: self.editar_linha(row))
                btn_excluir = QPushButton('Excluir')
                btn_excluir.clicked.connect(lambda ch, row=rowIndex: self.excluir_linha(row))
                layout_acoes = QHBoxLayout()
                layout_acoes.addWidget(btn_editar)
                layout_acoes.addWidget(btn_excluir)
                cell_widget = QWidget()
                cell_widget.setLayout(layout_acoes)
                self.table.setCellWidget(rowIndex, 5, cell_widget)

    def editar_linha(self, row):
        dados_linha = [self.table.item(row, col).text() if self.table.item(row, col) else "" for col in range(self.table.columnCount() - 1)]
        dialog = EditarCadastroDialog(dados_linha, self)
        if dialog.exec():
            self.carregar_dados()  # Recarrega os dados após a edição

    def excluir_linha(self, row):
        resposta = QMessageBox.question(self, "Confirmar Exclusão", "Você tem certeza que deseja excluir esta linha?")
        if resposta == QMessageBox.Yes:
            titulo = self.table.item(row, 0).text()
            self.remover_linha_csv(titulo)
            self.carregar_dados()

    def remover_linha_csv(self, titulo):
        arquivo_csv = os.path.join('data', 'tarefas.csv')
        with open(arquivo_csv, 'r', newline='', encoding='utf-8') as csvfile:
            linhas = list(csv.reader(csvfile))
        with open(arquivo_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for linha in linhas:
                if linha[0] != titulo:
                    writer.writerow(linha)

    def salvar_edicao(self, titulo_original, novos_dados):
        self.remover_linha_csv(titulo_original)  # Remove a linha original
        arquivo_csv = os.path.join('data', 'tarefas.csv')
        with open(arquivo_csv, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(novos_dados)  # Adiciona a linha editada