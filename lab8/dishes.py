import psycopg2
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)


class dishes(QWidget):
    def __init__(self, database):
        super(dishes, self).__init__()
        self.conn = database
        self.cursor = self.conn.cursor()

        self._create_dishes_tab()

    def _create_dishes_tab(self):
        self.gbox = QGroupBox("Блюда")

        self.vbox = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()

        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)

        self.hbox1.addWidget(self.gbox)

        self._create_dishes_table()

        self.update_dishes_button = QPushButton("Обновить")
        self.hbox2.addWidget(self.update_dishes_button)
        self.update_dishes_button.clicked.connect(self._update_dishes_table)

        self.setLayout(self.vbox)

    def _create_dishes_table(self):
        self.dishes_table = QTableWidget()
        self.dishes_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.dishes_table.setColumnCount(4)
        self.dishes_table.setHorizontalHeaderLabels(["Название", "Цена", "ID кухни", ""])

        self.vbox_table = QVBoxLayout()
        self.vbox_table.addWidget(self.dishes_table)
        self.gbox.setLayout(self.vbox_table)

        self._update_dishes_table()

    def _update_dishes_table(self):
        self.cursor.execute("SELECT dish_name, dish_cost, fk_cuisine_id \
                             FROM dishes ORDER BY dish_cost")
        records = list(self.cursor.fetchall())
        self.dishes_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            changeButton = QPushButton("Изменить")

            self.dishes_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.dishes_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.dishes_table.setItem(i, 2, QTableWidgetItem(str(r[2])))

            self.dishes_table.setCellWidget(i, 3, changeButton)
            changeButton.clicked.connect(lambda ch, num=i, id=r[0]: self._change_dishes(num, id))

        self.dishes_table.setItem(len(records), 0, QTableWidgetItem(''))
        changeButton = QPushButton("Добавить")
        self.dishes_table.setCellWidget(len(records), 3, changeButton)
        changeButton.clicked.connect(lambda ch, row=len(records): self._add_record(row))

        self.dishes_table.resizeRowsToContents()

    def _change_dishes(self, rowNum, id):
        row = list()
        for i in range(self.dishes_table.columnCount() - 1):
            try:
                row.append(self.dishes_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            if row.count('') == self.dishes_table.columnCount() - 1:
                self.cursor.execute(f"DELETE FROM dishes WHERE dish_name='{id}'")
            else:
                self.cursor.execute(f"UPDATE dishes SET dish_name='{row[0]}', dish_cost='{row[1]}', fk_cuisine_id='{row[2]}'\
                                    WHERE dish_name='{id}'")
            self.conn.commit()
        except BaseException as E:
            QMessageBox.about(self, "Error", str(E))
            self.conn.rollback()
        finally:
            self._update_dishes_table()

    def _add_record(self, row):
        try:
            self.cursor.execute(f"INSERT INTO dishes (dish_name, dish_cost, fk_cuisine_id)\
                                VALUES ('{self.dishes_table.item(row, 0).text()}', '{self.dishes_table.item(row, 1).text()}', '{self.dishes_table.item(row, 2).text()}')")
            self.conn.commit()
        except BaseException as E:
            QMessageBox.about(self, "Error", str(E))
            self.conn.rollback()
        finally:
            self._update_dishes_table()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="mvpe86qw",
                            host="localhost",
                            port="5432")
    cursor = conn.cursor()
    win = dishes(conn)
    win.showMaximized()
    sys.exit(app.exec_())