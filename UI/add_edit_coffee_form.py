from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton, QStatusBar


class AddEditCoffeeForm(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        
        self.setGeometry(0, 0, 405, 426)
        
        self.label = QLabel(self)
        self.label.setText("Название сорта")
        self.label.setGeometry(10, 30, 101, 31)
        
        self.sort_name = QLineEdit(self)
        self.sort_name.setGeometry(110, 39, 271, 21)
        
        self.label_2 = QLabel(self)
        self.label_2.setText("Степень обжарки")
        self.label_2.setGeometry(10, 60, 101, 31)

        self.roasting_degree = QComboBox(self)
        self.roasting_degree.setGeometry(110, 70, 271, 22)
        
        self.label_3 = QLabel(self)
        self.label_3.setText("Молотый/в зернах")
        self.label_3.setGeometry(10, 90, 101, 31)
        
        self.ground_or_in_grains = QComboBox(self)
        self.ground_or_in_grains.setGeometry(110, 100, 271, 22)
        
        self.label_4 = QLabel(self)
        self.label_4.setText("Описание вкуса")
        self.label_4.setGeometry(10, 120, 101, 31)
        
        self.taste_description = QTextEdit(self)
        self.taste_description.setGeometry(110, 130, 271, 81)
        
        self.label_5 = QLabel(self)
        self.label_5.setText("Цена")
        self.label_5.setGeometry(10, 220, 101, 31)
        
        self.price = QLineEdit(self)
        self.price.setGeometry(110, 230, 271, 21)
        
        self.label_6 = QLabel(self)
        self.label_6.setText("Объем упаковки")
        self.label_6.setGeometry(10, 260, 101, 31)
        
        self.packing_volume = QLineEdit(self)
        self.packing_volume.setGeometry(110, 270, 271, 21)
        
        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(214, 330, 161, 31)
        
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
