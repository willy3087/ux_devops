from PyQt5.QtWidgets import QMainWindow, QMenuBar, QAction, QStackedWidget, QWidget, QVBoxLayout, QPushButton, QMessageBox
from formularios.form_tarefa import FormularioTarefa
from formularios.form_correcao import FormularioCorrecao
from formularios.padronizacao import FormularioPadronizacao
from utils.visualizacao_tarefas import VisualizacaoTarefas
from configuracoes.config_window import ConfigWindow
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

class TelaInicial(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.btn_tarefas = QPushButton("Tarefas")
        self.btn_correcoes = QPushButton("Correções")
        self.btn_padronizacao = QPushButton("Padronização")

        layout.addWidget(self.btn_tarefas)
        layout.addWidget(self.btn_correcoes)
        layout.addWidget(self.btn_padronizacao)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestão de Tarefas")
        self.setGeometry(100, 100, 800, 600)
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.tela_inicial = TelaInicial()
        self.form_tarefa = FormularioTarefa()
        self.form_correcao = FormularioCorrecao()
        self.padronizacao = FormularioPadronizacao()
        
        self.stacked_widget.addWidget(self.tela_inicial)
        self.stacked_widget.addWidget(self.form_tarefa)
        self.stacked_widget.addWidget(self.form_correcao)
        self.stacked_widget.addWidget(self.padronizacao)
        
        self.tela_inicial.btn_tarefas.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.form_tarefa))
        self.tela_inicial.btn_correcoes.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.form_correcao))
        self.tela_inicial.btn_padronizacao.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.padronizacao))

        self.menu_bar = self.menuBar()
        self.menu_bar.setNativeMenuBar(False)
        self.init_ui()
        self.criar_menus()
        
     #Retorno a tela inicial 
        
    def init_ui(self):
        self.form_tarefa = FormularioTarefa()
        self.form_correcao = FormularioCorrecao()
        self.visualizacao_tarefas = VisualizacaoTarefas()
        self.config_window = ConfigWindow()
        self.padronizacao = FormularioPadronizacao()

        self.stacked_widget.addWidget(self.form_tarefa)
        self.stacked_widget.addWidget(self.form_correcao)
        self.stacked_widget.addWidget(self.visualizacao_tarefas)
        self.stacked_widget.addWidget(self.config_window)
        self.stacked_widget.addWidget(self.padronizacao)
        self.form_tarefa.sinal_voltar.connect(self.voltar_para_tela_inicial)
        self.form_correcao.sinal_voltar.connect(self.voltar_para_tela_inicial)
        self.padronizacao.sinal_voltar.connect(self.voltar_para_tela_inicial)
        
    def voltar_para_tela_inicial(self):
        self.stacked_widget.setCurrentWidget(self.tela_inicial)  

    def criar_menus(self):
        cadastro_menu = self.menu_bar.addMenu("Cadastro")
        lista_menu = self.menu_bar.addMenu("Lista de Tarefas")
        configuracoes_menu = self.menu_bar.addMenu("Configurações")

        # Ações do menu Cadastro
        tarefa_action = QAction("Cadastrar Tarefa", self)
        tarefa_action.triggered.connect(self.abrir_formulario_tarefa)
        cadastro_menu.addAction(tarefa_action)

        correcao_action = QAction("Cadastrar Correção", self)
        correcao_action.triggered.connect(self.abrir_formulario_correcao)
        cadastro_menu.addAction(correcao_action)

        # Ação do menu Lista de Tarefas
        lista_action = QAction("Visualizar Tarefas", self)
        lista_action.triggered.connect(self.abrir_lista_tarefas)
        lista_menu.addAction(lista_action)

        # Ação do menu Configurações
        config_action = QAction("Configurações", self)
        config_action.triggered.connect(self.abrir_configuracoes)
        configuracoes_menu.addAction(config_action)

    def abrir_formulario_tarefa(self):
        self.form_tarefa = FormularioTarefa()
        self.form_tarefa.show()

    def abrir_formulario_correcao(self):
        self.form_correcao = FormularioCorrecao()
        self.form_correcao.show()

    def abrir_lista_tarefas(self):
        self.visualizacao_tarefas = VisualizacaoTarefas()
        self.visualizacao_tarefas.show()

    def abrir_configuracoes(self):
        self.config_window = ConfigWindow()
        self.config_window.show()