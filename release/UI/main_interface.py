from PyQt6.QtWidgets import QMainWindow, QPushButton, QTableWidget, QStatusBar, QFrame, QVBoxLayout


class MainInterface(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        self.setGeometry(0, 0, 1200, 750)
        self.setWindowTitle("Информация о кофе")
        
        self.frame = QFrame(self)
        self.setCentralWidget(self.frame)
        
        layout = QVBoxLayout(self.frame)
        
        self.addButton = QPushButton("Добавить элемент")
        self.changeButton = QPushButton("Изменить элемент")
        self.coffeeTable = QTableWidget()
        
        layout.addWidget(self.addButton)
        layout.addWidget(self.changeButton)
        layout.addWidget(self.coffeeTable)
        
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
