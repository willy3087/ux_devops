from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QTextEdit
import csv
import os
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout

class FormularioTarefa(QWidget):
    sinal_salvar = pyqtSignal()
    sinal_voltar = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro de Tarefa")
        self.setGeometry(100, 100, 400, 600)  # Ajuste na altura para acomodar os novos campos
        self.init_ui()
        self.carregar_clientes()
        self.carregar_sprints()

    def init_ui(self):
        layout = QVBoxLayout()

        # Criando os widgets
        self.label_titulo = QLabel('Título da Tarefa:')
        self.input_titulo = QLineEdit()

        self.label_problema = QLabel('Descrição do Problema:')
        self.input_problema = QTextEdit()

        self.label_prioridade = QLabel('Prioridade:')
        self.combo_prioridade = QComboBox()
        self.combo_prioridade.addItems(['1 - Muito Urgente', '2 - Urgente', '3 - Moderado', '4 - Baixo', '5 - Nada Urgente'])

        # Adicionando selects para clientes e sprints
        self.label_cliente = QLabel('Cliente:')
        self.combo_cliente = QComboBox()
        layout.addWidget(self.label_cliente)
        layout.addWidget(self.combo_cliente)

        self.label_sprint = QLabel('Sprint Atual:')
        self.combo_sprint = QComboBox()
        layout.addWidget(self.label_sprint)
        layout.addWidget(self.combo_sprint)

        self.label_responsavel = QLabel('Responsável:')
        self.input_responsavel = QLineEdit()

        self.label_contato = QLabel('Ponto de Contato:')
        self.input_contato = QLineEdit()

        self.label_objetivo = QLabel('Objetivo:')
        self.input_objetivo = QTextEdit()

        self.btn_enviar = QPushButton('Enviar')
        self.btn_voltar = QPushButton('Voltar')  # Botão Voltar
        self.btn_enviar.clicked.connect(self.salvar_tarefa)
        self.btn_voltar.clicked.connect(lambda: self.sinal_voltar.emit())  # Emite o sinal para voltar

        # Organizando os widgets no layout
        layout.addWidget(self.label_titulo)
        layout.addWidget(self.input_titulo)
        layout.addWidget(self.label_problema)
        layout.addWidget(self.input_problema)
        layout.addWidget(self.label_prioridade)
        layout.addWidget(self.combo_prioridade)
        layout.addWidget(self.label_responsavel)
        layout.addWidget(self.input_responsavel)
        layout.addWidget(self.label_contato)
        layout.addWidget(self.input_contato)
        layout.addWidget(self.label_objetivo)
        layout.addWidget(self.input_objetivo)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_enviar)
        btn_layout.addWidget(self.btn_voltar)
        
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def carregar_clientes(self):
        try:
            with open('data/clientes.txt', 'r') as f:
                clientes = f.readlines()
            for cliente in clientes:
                self.combo_cliente.addItem(cliente.strip())
        except FileNotFoundError:
            pass  # Trate como achar melhor

    def carregar_sprints(self):
        try:
            with open('data/sprints.txt', 'r') as f:
                sprints = f.readlines()
            for sprints in sprints:
                # Adiciona apenas a última sprint
                self.combo_sprint.addItem(sprints.strip())
        except FileNotFoundError:
            pass  # Trate como achar melhor
    
    def salvar_tarefa(self):
        titulo = self.input_titulo.text()
        descricao = self.input_problema.toPlainText()
        prioridade = self.combo_prioridade.currentText()
        cliente = self.combo_cliente.currentText()
        sprint = self.combo_sprint.currentText()

        # Verifica se os campos não estão vazios
        if not titulo or not descricao:
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos.")
            return

        # Verifica a restrição de prioridade
        if not self.pode_salvar_prioridade(cliente, sprint, prioridade):
            QMessageBox.warning(self, "Erro", "Já existe uma tarefa com essa prioridade para o cliente e sprint selecionados.")
            return

        # Caminho para o arquivo CSV
        arquivo_csv = os.path.join('data', 'tarefas.csv')

        # Cria o diretório 'data' se ele não existir
        os.makedirs(os.path.dirname(arquivo_csv), exist_ok=True)

        # Escreve no arquivo CSV
        try:
            with open(arquivo_csv, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([titulo, descricao, prioridade, cliente, sprint])
            QMessageBox.information(self, "Sucesso", "Tarefa salva com sucesso.")
            self.sinal_retorno_tela_inicial.emit()  # Emitir sinal para retornar à tela inicial
            self.input_titulo.clear()
            self.input_problema.clear()
            self.input_responsavel.clear()
            self.input_contato.clear()
            self.input_objetivo.clear()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Não foi possível salvar a tarefa: {e}")

    def pode_salvar_prioridade(self, cliente, sprint, prioridade):
        if prioridade == '5':
            return True  # Sempre permite prioridade 5

        arquivo_csv = os.path.join('data', 'tarefas.csv')
        try:
            with open(arquivo_csv, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    # Supondo que as colunas estejam na ordem: titulo, descricao, prioridade, cliente, sprint
                    _, _, prioridade_existente, cliente_existente, sprint_existente = row
                    if cliente == cliente_existente and sprint == sprint_existente and prioridade == prioridade_existente:
                        return False  # Já existe uma tarefa com essa prioridade para o cliente e sprint
        except FileNotFoundError:
            pass  # Se o arquivo não existir, não há tarefas salvas, então pode salvar

        return True