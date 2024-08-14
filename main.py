from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QLineEdit, QPushButton,
                             QMainWindow, QTableWidget, QTableWidgetItem,
                             QDialog, QComboBox, QToolBar, QStatusBar,
                             QGridLayout, QLabel, QMessageBox)
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


# The class QMainWindow made possible the insertion of the upper menu
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Name the window
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        # Added the upper menu
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Add the sub option "Add Student" into the option "File"
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student",
                                     self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        # Add the sub option "About "into the option "Help"
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        about_action.triggered.connect(self.about)

        # Add the sub option "Search" into the option "Edit"
        search_student_action = QAction(QIcon("icons/search.png"), "Search",
                                        self)
        search_student_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_student_action)

        # Made the table that would display the students information
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name",
                                              "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create a toolbar and it`s elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)

        # Create status bar and add it`s elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        # The purpose of this is finding objects of QPushButton and delete it
        # before the new buttons are added, to avoid the repetition.
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

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
    @staticmethod
    def insert():
        dialog = InsertDialog()
        dialog.exec()

    # Function to connect the Main Window to the Search Student Window
    @staticmethod
    def search():
        dialog = SearchDialog()
        dialog.exec()

    @staticmethod
    def edit():
        dialog = EditDialog()
        dialog.exec()

    @staticmethod
    def delete():
        dialog = DeleteDialog()
        dialog.exec()

    @staticmethod
    def about():
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        VASCO DA GAMA
        """
        self.setText(content)


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
        self.close()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name text box widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name:")
        layout.addWidget(self.student_name)

        # Add "Search button widget"
        button = QPushButton("Search")
        button.clicked.connect(self.search_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def search_student(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        # It's necessary that name is written as (name, ) because the execute()
        # method expect a tuple
        result = cursor.execute("select * from students where name = ?",
                                (name,))
        items = main_window.table.findItems(name,
                                            Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)
        cursor.close()
        connection.close()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Get student name from selected row
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()

        # Get ID from selected row
        self.student_id = main_window.table.item(index, 0).text()

        # Add student name widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name:")
        layout.addWidget(self.student_name)

        course_name = main_window.table.item(index, 2).text()

        # Add courses combobox widget
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        mobile = main_window.table.item(index, 3).text()

        # Add mobile widget
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile:")
        layout.addWidget(self.mobile)

        # Add submit button
        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("update students set name = ?, course = ?, "
                       "mobile = ? where id = ?",
                       (self.student_name.text(),
                        self.course_name.currentText(), self.mobile.text(),
                        self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        # Refresh the table
        main_window.load_data()
        self.close()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes_button, 1, 0)
        layout.addWidget(no_button, 1, 1)

        yes_button.clicked.connect(self.delete_student)

        self.setLayout(layout)

    def delete_student(self):
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("delete from students where id = ?",
                       (student_id, ))

        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success!")
        confirmation_widget.setText("The record was deleted successfully!")
        confirmation_widget.exec()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
