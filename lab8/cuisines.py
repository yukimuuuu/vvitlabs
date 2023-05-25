import psycopg2
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)

class Cuisines(QWidget):
    def __init__(self, database):
        super(Cuisines, self).__init__()
        self.conn = database
        self.cursor = self.conn.cursor()

        self._create_cuisines_tab()

    def _create_cuisines_tab(self):
        self.gbox = QGroupBox("Кухни")

        self.vbox = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()

        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)

        self.hbox1.addWidget(self.gbox)

        self._create_cuisines_table()

        self.update_cuisines_button = QPushButton("Обновить")
        self.hbox2.addWidget(self.update_cuisines_button)
        self.update_cuisines_button.clicked.connect(self._update_cuisines_table)

        self.setLayout(self.vbox)

    def _create_cuisines_table(self):
        self.cuisines_table = QTableWidget()
        self.cuisines_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.cuisines_table.setColumnCount(3)
        self.cuisines_table.setHorizontalHeaderLabels(["Id", "Название кухни", ""])

        self.vbox_cuisines = QVBoxLayout()
        self.vbox_cuisines.addWidget(self.cuisines_table)
        self.gbox.setLayout(self.vbox_cuisines)

        self._update_cuisines_table()

    def _update_cuisines_table(self):

        self.cursor.execute("SELECT *\
                             FROM cuisines ORDER BY cuisine_id")
        records = list(self.cursor.fetchall())
        self.cuisines_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            changeButton = QPushButton("Изменить")

            self.cuisines_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.cuisines_table.setItem(i, 1, QTableWidgetItem(str(r[1])))

            self.cuisines_table.setCellWidget(i, 2, changeButton)
            changeButton.clicked.connect(lambda ch, num=i, id=r[0]: self._change_cuisines(num, id))

        self.cuisines_table.setItem(len(records), 0, QTableWidgetItem(''))
        self.cuisines_table.setItem(len(records), 1, QTableWidgetItem(''))
        changeButton = QPushButton("Добавить")
        self.cuisines_table.setCellWidget(len(records), 2, changeButton)
        changeButton.clicked.connect(lambda ch, row=len(records): self._add_record(row))

        self.cuisines_table.resizeRowsToContents()

    def _change_cuisines(self, rowNum, id):
        row = list()
        for i in range(self.cuisines_table.columnCount() - 1):
            try:
                row.append(self.cuisines_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            if row.count('') == self.cuisines_table.columnCount() - 1:
                self.cursor.execute(f"DELETE FROM cuisines WHERE cuisine_id={id}")
            else:
                self.cursor.execute(f"UPDATE cuisines SET cuisine_name='{row[1]}' WHERE cuisine_id={id}")
            self.conn.commit()
        except BaseException as E:
            QMessageBox.about(self, "Error", str(E))
            self.conn.rollback()
        finally:
            self._update_cuisines_table()

    def _add_record(self, row):
        data = [self.cuisines_table.item(row, 0).text(),
                self.cuisines_table.item(row, 1).text()]
        try:
            self.cursor.execute(f"INSERT INTO cuisines (cuisine_id, cuisine_name)\
                                VALUES ('{data[0]}', '{data[1]}')")
            self.conn.commit()
        except BaseException as E:
            QMessageBox.about(self, "Error", str(E))
            self.conn.rollback()
        finally:
            self._update_cuisines_table()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="mvpe86qw",
                            host="localhost",
                            port="5432")
    cursor = conn.cursor()
    win = Cuisines(conn)
    win.showMaximized()
    sys.exit(app.exec_())