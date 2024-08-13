from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QLabel, QWidget,
                             QGridLayout, QLineEdit, QPushButton, QMainWindow,
                             QTableWidget, QTableWidgetItem, QDialog,
                             QComboBox)
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
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Add the sub option "Add Student" into the option "File"
        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        # Add the sub option "About "into the option "Help"
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        # Add the sub option "Search" into the option "Edit"
        search_student_action = QAction("Search", self)
        search_student_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_student_action)

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

    # Function to connect the Main Window to the Add Student Window
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    # Function to connect the Main Window to the Search Student Window
    def search(self):
        dialog = SearchDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name:")
        layout.addWidget(self.student_name)

        # Add courses combobox widget
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile:")
        layout.addWidget(self.mobile)

        # Add submit button
        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("insert into students (name, course, mobile)"
                       " values (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()

        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name text box widget
        student_name = QLineEdit()
        student_name.setPlaceholderText("Name:")
        layout.addWidget(student_name)

        # Add "Search button widget"
        button = QPushButton("Search")
        layout.addWidget(button)

        self.setLayout(layout)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
