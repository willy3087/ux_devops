from PyQt5.QtWidgets import QApplication
from interface.main_window import MainWindow  # Ajuste o caminho do import conforme a estrutura do seu projeto
import sys

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()