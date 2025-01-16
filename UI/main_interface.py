from PyQt6.QtWidgets import QMainWindow, QPushButton, QTableWidget, QStatusBar


class MainInterface(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        self.setGeometry(0, 0, 640, 480)
        self.setWindowTitle("Информация о кофе")
        
        self.addButton = QPushButton(self)
        self.addButton.setText("Добавить элемент")
        self.addButton.setGeometry(10, 10, 191, 31)
        
        self.changeButton = QPushButton(self)
        self.changeButton.setText("Изменить элемент")
        self.changeButton.setGeometry(210, 10, 191, 31)
        
        self.coffeeTable = QTableWidget(self)
        self.coffeeTable.setGeometry(0, 50, 641, 391)
        
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
