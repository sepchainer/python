import sys
import webbrowser
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Fenster(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        self.label = QLabel(self)
        self.label.setText('Suche:')
        self.line = QLineEdit(self)
        self.setStyleSheet("background-color: grey;")

        self.line.move(100, 100)
        self.line.resize(200, 40)
        self.label.move(50, 105)
        button = QPushButton("Suche",self)
        button.move(310,105)
        button.clicked.connect(self.geizhals_suche)

        self.setGeometry(100, 100, 500, 300)
        self.setWindowTitle("Geizhals Suche")
        self.show()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Return:
            self.geizhals_suche()

    def geizhals_suche(self):
        search = self.line.text()
        split_eingabe = search.split()
        plus = '+'
        split_eingabe_plus = plus.join(split_eingabe)

        url = 'https://geizhals.at/?fs=' + split_eingabe_plus + '&hloc=at&in='

        webbrowser.open(url)

app = QApplication(sys.argv)
w = Fenster()
sys.exit(app.exec_())
