import psycopg2
import sys

from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget, QVBoxLayout)


from restaurants import Restaurants
from cuisines import Cuisines
from dishes import dishes

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()
        self.setWindowTitle("schedule_db")

        self.vbox = QVBoxLayout(self)
        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self.restaurants_tab = Restaurants(self.conn)
        self.tabs.addTab(self.restaurants_tab, 'Рестораны')

        self.cuisines_tab = Cuisines(self.conn)
        self.tabs.addTab(self.cuisines_tab, 'Кухни')

        self.dishes_tab = dishes(self.conn)
        self.tabs.addTab(self.dishes_tab, 'Блюда')

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="postgres",
                                     user="postgres",
                                     password="mvpe86qw",
                                     host="localhost",
                                     port="5432")
        self.cursor = self.conn.cursor()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.showMaximized()
    sys.exit(app.exec_())