import psycopg2
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)

class Restaurants(QWidget):
    def __init__(self, database):
        super(Restaurants, self).__init__()
        self.conn = database
        self.cursor = self.conn.cursor()

        self._create_restaurants_tab()

    def _create_restaurants_tab(self):
        self.gbox = QGroupBox("Кухни")

        self.vbox = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()

        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)

        self.hbox1.addWidget(self.gbox)

        self._create_restaurants_table()

        self.update_restaurants_button = QPushButton("Обновить")
        self.hbox2.addWidget(self.update_restaurants_button)
        self.update_restaurants_button.clicked.connect(self._update_restaurants_table)

        self.setLayout(self.vbox)

    def _create_restaurants_table(self):
        self.restaurants_table = QTableWidget()
        self.restaurants_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.restaurants_table.setColumnCount(5)
        self.restaurants_table.setHorizontalHeaderLabels(["Id", "Название ресторана", "Местоположение", "Звезды Мишлен", ""])

        self.vbox_restaurants = QVBoxLayout()
        self.vbox_restaurants.addWidget(self.restaurants_table)
        self.gbox.setLayout(self.vbox_restaurants)

        self._update_restaurants_table()

    def _update_restaurants_table(self):

        self.cursor.execute("SELECT *\
                             FROM restaurants ORDER BY restaurant_id")
        records = list(self.cursor.fetchall())
        self.restaurants_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            changeButton = QPushButton("Изменить")

            self.restaurants_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.restaurants_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.restaurants_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.restaurants_table.setItem(i, 3, QTableWidgetItem(str(r[3])))

            self.restaurants_table.setCellWidget(i, 4, changeButton)
            changeButton.clicked.connect(lambda ch, num=i, id=r[0]: self._change_restaurants(num, id))

        self.restaurants_table.setItem(len(records), 0, QTableWidgetItem(''))
        self.restaurants_table.setItem(len(records), 1, QTableWidgetItem(''))
        changeButton = QPushButton("Добавить")
        self.restaurants_table.setCellWidget(len(records), 4, changeButton)
        changeButton.clicked.connect(lambda ch, row=len(records): self._add_record(row))

        self.restaurants_table.resizeRowsToContents()

    def _change_restaurants(self, rowNum, id):
        row = list()
        for i in range(self.restaurants_table.columnCount() - 1):
            try:
                row.append(self.restaurants_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            if row.count('') == self.restaurants_table.columnCount() - 1:
                self.cursor.execute(f"DELETE FROM restaurants WHERE restaurant_id={id}")
            else:
                self.cursor.execute(f"UPDATE restaurants SET restaurant_name='{row[1]}', restaurant_location='{row[2]}', restaurant_stars='{row[3]}'\
                                    WHERE restaurant_id={id}")
            self.conn.commit()
        except BaseException as E:
            QMessageBox.about(self, "Error", str(E))
            self.conn.rollback()
        finally:
            self._update_restaurants_table()

    def _add_record(self, row):
        data = [self.restaurants_table.item(row, 0).text(),
                self.restaurants_table.item(row, 1).text(),
                self.restaurants_table.item(row, 2).text(),
                self.restaurants_table.item(row, 3).text()]
        try:
            self.cursor.execute(f"INSERT INTO restaurants (restaurant_id, restaurant_name, restaurant_location, restaurant_stars)\
                                VALUES ('{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}')")
            self.conn.commit()
        except BaseException as E:
            QMessageBox.about(self, "Error", str(E))
            self.conn.rollback()
        finally:
            self._update_restaurants_table()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="mvpe86qw",
                            host="localhost",
                            port="5432")
    cursor = conn.cursor()
    win = Restaurants(conn)
    win.showMaximized()
    sys.exit(app.exec_())