from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QLabel, QWidget,\
    QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget,
    QTableWidgetItem)
from PyQt6.QtGui import QAction
import sys
import sqlite3


# The class QMainWindow made possible the insertion of the upper menu
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Name the window
        self.setWindowTitle("Student Management System")

        # Added the upper menu
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        # Add a sub option into the option "File"
        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)

        # Add a sub option into the option "Help"
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        # Made the table that would display the students informations
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name",
                                             "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        # Connection with the SQLite database
        connection = sqlite3.connect("database.db")
        # Command to consult the database and save the infos into the variable
        # result
        result = connection.execute("select * from students")
        # Restarts the table
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                # Generates coordinates to add the extracted data
                self.table.setItem(row_number, column_number,
                                   QTableWidgetItem(str(data)))
        connection.close()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())

