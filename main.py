import sys
import sqlite3

from UI.main_interface import MainInterface
from UI.add_edit_coffee_form import AddEditCoffeeForm

from PyQt6.QtWidgets import QApplication, QTableWidgetItem


class MyWidget(MainInterface):
    def __init__(self) -> None:
        super().__init__()
        
        self.initUi()
        
    def initUi(self) -> None:
        self.addButton.clicked.connect(self.add_coffee)
        self.changeButton.clicked.connect(self.change_coffee)
        
        self.conn = sqlite3.connect("data/coffee.sqlite")
        self.cur = self.conn.cursor()
        
        self.update_info()
    
    def update_info(self) -> None:
        result = self.cur.execute(
            """
            SELECT coffee_information.ID, coffee_information.sort_name,
            roasting.type, ground_grains.type,
            coffee_information.taste_description, coffee_information.price,
            coffee_information.packing_volume
            FROM coffee_information
            JOIN ground_grains ON coffee_information.ground_or_in_grains = ground_grains.ID
            JOIN roasting ON coffee_information.roasting_degree = roasting.ID
            """
        )
        
        table_labels = ["ID", "Название сорта", "Степень обжарки", "Молотый/в зернах",
                        "Описание вкуса", "Цена", "Объем упаковки"]
        
        self.coffeeTable.setColumnCount(len(table_labels))
        self.coffeeTable.setRowCount(0)
        
        self.coffeeTable.setHorizontalHeaderLabels(table_labels)
        
        for i, row in enumerate(result):
            self.coffeeTable.setRowCount(self.coffeeTable.rowCount() + 1)
            for j, elem in enumerate(row):
                self.coffeeTable.setItem(i, j, QTableWidgetItem(str(elem)))

        self.coffeeTable.resizeColumnsToContents()

    def add_coffee(self) -> None:
        self.add_coffee_widget = AddCoffeWidget(self)
        self.add_coffee_widget.show()
        
    def change_coffee(self) -> None:
        selected = self.coffeeTable.selectedItems()
        
        if not selected:
            self.statusbar.showMessage("Ничего не выбрано")
            return
        else:
            self.statusbar.clearMessage()
            
        coffee_id = int(self.coffeeTable.item(selected[0].row(), 0).text())
        self.edit_coffee_widget = AddCoffeWidget(self, coffee_id=coffee_id)
        self.edit_coffee_widget.show()


class AddCoffeWidget(AddEditCoffeeForm):
    def __init__(self, parent=None, coffee_id=None) -> None:
        super().__init__()
        self.parent_widget = parent
        
        self.initUi()
        
        self.coffee_id = coffee_id
        
        if coffee_id is not None:
            self.pushButton.clicked.disconnect()
            self.pushButton.clicked.connect(self.edit_coffee)
            self.pushButton.setText("Отредактировать")
            self.setWindowTitle("Редактирование записи")
            
            coffee_data = self.cur.execute("SELECT * From coffee_information WHERE ID = ?",
                                           (coffee_id,)).fetchone()

            self.sort_name.setText(coffee_data[1])
            
            roasting_degree_id = coffee_data[2]
            roasting_degree_name = next((name for name, id in self.roasting_degree_params.items() if id == roasting_degree_id), "")
            
            if roasting_degree_name:
                self.roasting_degree.setCurrentText(roasting_degree_name)
                
            ground_grains_id = coffee_data[3]
            ground_grains_name = next((name for name, id in self.ground_grains_params.items() if id == ground_grains_id), "")
            
            if ground_grains_name:
                self.ground_or_in_grains.setCurrentText(ground_grains_name)
            
            self.taste_description.setText(coffee_data[4])
            self.price.setText(str(coffee_data[5]))
            self.packing_volume.setText(str(coffee_data[6]))
        else:
            self.setWindowTitle("Добавление записи")
    
    def initUi(self) -> None:
        self.pushButton.clicked.connect(self.add_coffee)
        self.conn = sqlite3.connect("data/coffee.sqlite")
        self.cur = self.conn.cursor()
        
        roasting_degree_list = self.cur.execute("SELECT * FROM roasting").fetchall()
        self.roasting_degree_params = {title: id for id, title in roasting_degree_list}
        
        for roasting_degree in self.roasting_degree_params:
            self.roasting_degree.addItem(roasting_degree)
        
        ground_grains_list = self.cur.execute("SELECT * FROM ground_grains").fetchall()
        self.ground_grains_params = {title: id for id, title in ground_grains_list}
        
        for ground_grain in self.ground_grains_params:
            self.ground_or_in_grains.addItem(ground_grain)
    
    def add_coffee(self) -> None:
        try:
            sort_name = self.sort_name.text()
            roasting_degree = self.roasting_degree_params[self.roasting_degree.currentText()]
            ground_or_grains = self.ground_grains_params[self.ground_or_in_grains.currentText()]
            taste_description = self.taste_description.toPlainText()
            price = int(self.price.text())
            packing_volume = int(self.packing_volume.text())
            
            if not sort_name or (price <= 0) or (packing_volume <= 0):
                raise ValueError
            
            self.cur.execute(
                """
                INSERT INTO coffee_information(sort_name, roasting_degree, ground_or_in_grains, taste_description, price, packing_volume)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (sort_name, roasting_degree, ground_or_grains, taste_description, price, packing_volume)
            )
            self.conn.commit()
            self.parent_widget.update_info()
            self.close()
            
        except ValueError:
            self.statusbar.showMessage("Неверно заполнена форма")
    
    def edit_coffee(self) -> None:
        try:
            sort_name = self.sort_name.text()
            roasting_degree = self.roasting_degree_params[self.roasting_degree.currentText()]
            ground_or_grains = self.ground_grains_params[self.ground_or_in_grains.currentText()]
            taste_description = self.taste_description.toPlainText()
            price = int(self.price.text())
            packing_volume = int(self.packing_volume.text())
            
            if not sort_name or (price <= 0) or (packing_volume <= 0):
                raise ValueError
            
            self.cur.execute(
                """
                UPDATE coffee_information
                SET sort_name = ?,
                roasting_degree = ?,
                ground_or_in_grains = ?,
                taste_description = ?,
                price = ?,
                packing_volume = ?
                WHERE ID = ?
                """,
                (sort_name, roasting_degree, ground_or_grains, taste_description, price, packing_volume, self.coffee_id)
            )
            self.conn.commit()
            self.parent_widget.update_info()
            
            parent = self.parent_widget
            
            for row in range(parent.coffeeTable.rowCount()):
                if int(parent.coffeeTable.item(row, 0).text()) == self.coffee_id:
                    parent.coffeeTable.selectRow(row)
                    break
            
            self.close()
            
        except ValueError:
            self.statusbar.showMessage("Неверно заполнена форма")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_window = MyWidget()
    my_window.show()
    sys.exit(app.exec())
