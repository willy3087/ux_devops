from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget
import os

class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configurações")
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()
        self.carregar_dados_salvos()  # Carrega os dados salvos ao iniciar

    def init_ui(self):
        layout = QVBoxLayout()
        self.cliente_input = QLineEdit()
        self.cliente_lista = QListWidget()
        self.sprint_input = QLineEdit()
        self.sprint_lista = QListWidget()
        
        layout.addWidget(QLabel("Cliente"))
        layout.addWidget(self.cliente_input)
        self.submit_button_cliente = QPushButton("Adicionar Cliente")
        layout.addWidget(self.submit_button_cliente)
        layout.addWidget(self.cliente_lista)
        
        layout.addWidget(QLabel("Sprint"))
        layout.addWidget(self.sprint_input)
        self.submit_button_sprint = QPushButton("Adicionar Sprint")
        layout.addWidget(self.submit_button_sprint)
        layout.addWidget(self.sprint_lista)
        
        self.setLayout(layout)
        
        self.submit_button_cliente.clicked.connect(self.adicionar_cliente)
        self.submit_button_sprint.clicked.connect(self.adicionar_sprint)

    def carregar_dados_salvos(self):
        # Carrega clientes salvos
        if os.path.exists('data/clientes.txt'):
            with open('data/clientes.txt', 'r') as f:
                for cliente in f:
                    self.cliente_lista.addItem(cliente.strip())
        
        # Carrega sprints salvos
        if os.path.exists('data/sprints.txt'):
            with open('data/sprints.txt', 'r') as f:
                for sprint in f:
                    self.sprint_lista.addItem(sprint.strip())

    def adicionar_cliente(self):
        cliente = self.cliente_input.text()
        if cliente:
            with open('data/clientes.txt', 'a') as f:
                f.write(cliente + '\n')
            self.cliente_lista.addItem(cliente)
            self.cliente_input.clear()

    def adicionar_sprint(self):
        sprint = self.sprint_input.text()
        if sprint:
            with open('data/sprints.txt', 'a') as f:
                f.write(sprint + '\n')
            self.sprint_lista.addItem(sprint)
            self.sprint_input.clear()