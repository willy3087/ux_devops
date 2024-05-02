from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget

class VisualizacaoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualização de Demandas")
        self.setGeometry(100, 100, 800, 600)  # Define a posição e dimensões da janela

        self.central_widget = QWidget()  # Widget central que contém todos os outros widgets
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.lista_demandas = QListWidget(self)
        self.layout.addWidget(self.lista_demandas)

        self.btn_exportar_csv = QPushButton('Exportar para CSV', self)
        self.btn_exportar_csv.clicked.connect(self.exportar_para_csv)
        self.layout.addWidget(self.btn_exportar_csv)
        

        # Aqui você pode adicionar a lógica para carregar as demandas na QListWidget
        # Exemplo: self.lista_demandas.addItem("Demanda 1")

    def exportar_para_csv(self):
        # Aqui você pode adicionar a lógica para exportar as demandas para um arquivo CSV
        print("Exportando demandas para CSV...")