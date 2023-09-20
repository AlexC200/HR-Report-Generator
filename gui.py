"""GUI Module for Employee Information

We provide a default form with common Employee information, then inherit and subclass
to create custom forms for each type.

Ira Woodring
Winter 2023
"""

import csv

from PyQt6 import QtWidgets
from PyQt6.QtCore import QAbstractTableModel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtWidgets import QLabel, QLineEdit, QMenu, QHeaderView, QTableView, QMainWindow, QAbstractItemView, \
    QPushButton, QVBoxLayout, QListWidget, QListWidgetItem, QComboBox

from employee import *
from typing import *


class HRTableModel(QAbstractTableModel):
    """The HRTableModel allows us to display our information in a QTableView."""
    def __init__(self, data) -> None:
        super(HRTableModel, self).__init__()
        self._columns = ["ID#", "Type", "Name", "Pay", "Email"]
        self._data = data

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> str:
        """Gives the header info in a format PyQt wants."""
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            # return f"Column {section + 1}"
            return self._columns[section]
        if orientation == Qt.Orientation.Vertical and role == Qt.ItemDataRole.DisplayRole:
            return f"{section + 1}"

    def data(self, index, role) -> str:
        """Returns the data at some table index."""
        if role == Qt.ItemDataRole.DisplayRole:
            e = self._data[index.row()]
            field = e.id_number
            if index.column() == 1:
                field = type(e).__name__
            if index.column() == 2:
                field = e.name
            if index.column() == 3:
                if isinstance(e, Salaried):
                    field = '${:,.2f}'.format(e.yearly)
                else:
                    field = '${:,.2f}'.format(e.hourly_wage)
            if index.column() == 4:
                field = e.email
            return field

    def rowCount(self, index) -> int:
        """Provides the way for PyQt to get our row count."""
        return len(self._data)

    def columnCount(self, index) -> int:
        """Provides the column count, as PyQt expects."""
        return len(self._columns)


class MainWindow(QMainWindow):
    """MainWindow will have menus and a central list widget."""
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Employee Management v1.0.0")
        self.resize(800, 600)
        self._data = []
        self.load_file()
        self._model = HRTableModel(self._data)
        self._table = QTableView()
        self._table.setModel(self._model)
        self._table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self._table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self._table.setAlternatingRowColors(True)
        self._header = self._table.horizontalHeader()
        self._header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.setCentralWidget(self._table)
        self._create_menu_bar()
        self._employee_form = None
        self._about_form = AboutForm()

    def _create_menu_bar(self) -> None:
        # Create the menus.
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        file_menu = QMenu("&File", self)
        edit_menu = QMenu("&Edit", self)
        help_menu = QMenu("&Help", self)
        self._exit_action = QAction("&Exit")
        self._exit_action.triggered.connect(exit)
        self._load_action = QAction("&Load HR Data")
        self._save_action = QAction("&Save HR Data")
        self._save_action.setShortcut('Ctrl+S')
        file_menu.addAction(self._load_action)
        self._load_action.setShortcut('Ctrl+O')
        self._load_action.triggered.connect(self.load_file)
        file_menu.addAction(self._save_action)
        file_menu.addAction(self._exit_action)
        self._edit_action = QAction("&Edit current employee")
        edit_menu.addAction(self._edit_action)
        self._edit_action.triggered.connect(self.edit_employee)
        self._edit_action.setShortcut('Ctrl+E')
        self._save_action.triggered.connect(self.save_file)
        self._about_action = QAction("About this software")
        self._about_action.triggered.connect(self.show_help)
        help_menu.addAction(self._about_action)
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(edit_menu)
        menu_bar.addMenu(help_menu)
        self.setMenuBar(menu_bar)

    def show_help(self) -> None:
        """Our 'help' form merely shows who wrote this, the version, and a description."""
        self._about_form.show()

    def data_to_rows(self) -> List[str]:
        """It is sometimes useful for us to have our model data as a list.  This method
        provides that feature."""
        data = []
        for e in self._data:
            row = [e.id_number, type(e).__name__, e.name]
            if isinstance(e, Salaried):
                row.append(str(e.yearly))
            else:
                row.append(str(e.hourly))
            row.append(e.email)
            data.append(row)
        return data

    def refresh_width(self) -> None:
        """Resize our table to fit our data width."""
        self._header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

    def edit_employee(self) -> None:
        """Update an employee object by populating the correct type of form with the selected type of
        employee data."""
        index = self._table.selectionModel().selectedIndexes()
        if not index:
            return
        index = index[0].row()
        if isinstance(self._data[index], Executive):
            self._employee_form = ExecutiveForm(self)
        if isinstance(self._data[index], Manager):
            self._employee_form = ManagerForm(self)
        if isinstance(self._data[index], Permanent):
            self._employee_form = PermanentForm(self)
        if isinstance(self._data[index], Temporary):
            self._employee_form = TempForm(self)

        self._employee_form.fill_in(index)
        self._employee_form.show()

    def load_file(self) -> None:
        """Read a representation of all of our Employees from a file and store in our
        _data variable.  The table will automatically be populated by this variable."""
        with open('./employee.data') as datafile:
            reader = csv.reader(datafile, quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                type = row[0]
                name = row[1]
                email = row[2]
                _image = row[3]
                if type == 'Executive':
                    salary = float(row[4])
                    role = int(row[5])
                    employee = Executive(name, email, salary, role)
                if type == 'Manager':
                    salary = float(row[4])
                    department = int(row[5])
                    print(Department.ACCOUNTING.value == 1)
                    employee = Manager(name, email, salary, department)
                if type == 'Temp':
                    hourly = float(row[4])
                    last_day = row[5]
                    employee = Temporary(name, email, hourly, last_day)
                if type == 'Permanent':
                    hourly = float(row[4])
                    hired_date = row[5]
                    employee = Permanent(name, email, hourly, hired_date)
                print(employee)
                self._data.append(employee)

    def save_file(self) -> None:
        """Save a representation of all the Employees to a file."""
        file = open("./employee.data", "w")
        for employee in self._data:
            file.write(type(employee).__name__+','+employee.__repr__()+'\n')


class EmployeeForm(QtWidgets.QWidget):
    """There will never be a generic employee form, but we don't want to repeat code,
    so we put it all here.  Each subtype of form will add to it."""
    def __init__(self, parent=None, employee: Employee = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._parent = parent   # missing in student version
        self._employee = employee   # missing in student version
        outer_layout = QVBoxLayout()
        self.layout = QtWidgets.QFormLayout()
        self.setLayout(outer_layout)
        self._id_label = QLabel()
        self.layout.addRow(QLabel("ID#"), self._id_label)
        self._name_edit = QLineEdit()
        self.layout.addRow(QLabel("Name: "), self._name_edit)
        self._pay_edit = QLineEdit()
        self._email_edit = QLineEdit()
        self.layout.addRow(QLabel("Email address:"), self._email_edit)
        self._image_path_edit = QLineEdit()
        self.layout.addRow(QLabel("Image path:"), self._image_path_edit)
        self._image = QLabel()
        self._image.setPixmap(QPixmap(Employee.IMAGE_PLACEHOLDER))
        self.layout.addWidget(self._image)
        update = QPushButton("Update")
        update.clicked.connect(self.update_employee)
        outer_layout.addLayout(self.layout)
        outer_layout.addWidget(update)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

    def update_employee(self) -> None:
        """Change the selected employee's data to the updated values."""
        try:
            self._employee.name = self._name_edit.text()
            self._employee.email = self._email_edit.text()
            self._employee.image = self._image_path_edit.text()
            self._parent.refresh_width()
            self.setVisible(False)
        except ValueError as message:
            print(message)

    def fill_in(self, index) -> None:
        """Upon opening the form, we wish to add the selected employee's data
        to the fields."""
        self._employee = self._parent._data[index]
        self.setWindowTitle("Edit " + type(self._employee).__name__ + " Employee Information")
        self._id_label.setText(str(self._employee.id_number))
        self._name_edit.setText(self._employee.name)
        self._email_edit.setText(self._employee.email)
        self._image_path_edit.setText(self._employee.image)
        self._image.setPixmap(QPixmap(self._employee.image))

# Complete the following forms so that they update and fill-in
# their custom information.


class SalariedForm(EmployeeForm):

    def fill_in(self, index):
        super().fill_in(index)
        self.salary_label = QLabel("Salary:", self)
        self._pay_edit.setText(str(self._employee.yearly))
        self.layout.addRow(self.salary_label, self._pay_edit)

    def update_employee(self) -> None:
        try:
            super().update_employee()
            self._employee.yearly = float(self._pay_edit.text())
            print("updated_yearly")
            self._parent.refresh_width()
            self.setVisible(False)
        except ValueError as message:
            print("Invalid data type")


class ExecutiveForm(SalariedForm):

    def fill_in(self, index):
        super().fill_in(index)
        self.role = QComboBox(self)
        for role in Role:
            self.role.addItem(role.name)
        self.layout.addRow(self.salary_label, self._pay_edit)

        self.layout.addRow(QLabel("Role", self), self.role)

    def update_employee(self) -> None:
        try:
            super().update_employee()
            self._parent.refresh_width()

            self.setVisible(False)
        except ValueError as message:
            print(message)


class ManagerForm(SalariedForm):

    def fill_in(self, index):
        super().fill_in(index)
        self.salary_label = QLabel("Salary:", self)
        self._pay_edit = QLineEdit(self)
        self.dept = QComboBox(self)
        for dept in Department:
            self.dept.addItem(dept.name)

        self.layout.addRow(QLabel("Department", self), self.dept)


class HourlyForm(EmployeeForm):

    def fill_in(self, index):
        super().fill_in(index)
        self.hourly_wage = QLabel('Hourly wage:')
        self._pay_edit.setText(str(self._employee.hourly_wage))
        self.layout.addRow(self.hourly_wage, self._pay_edit)

    def update_employee(self) -> None:
        try:
            super().update_employee()
            self._employee.hourly_wage = float(self._pay_edit.text())
            print("updated_hourly")
            self._parent.refresh_width()
            self.setVisible(False)
        except ValueError as message:
            print("Invalid data type")


"""creates a form for editing temporary employees...includes fields for 
the employee's name, address, hourly pay rate, hourly wage, and last day of work."""


class TempForm(HourlyForm):

    def __init__(self, employee=None):
        super().__init__(employee)
        self.hourly_wage_label = QLabel('Hourly')
        self.last_day_label = QLabel()
        self.layout.addWidget(QLabel('Last day:'))

    def fill_in(self, index):
        super().fill_in(index)
        self.layout.addRow(QLabel("Last Day " + str(self._employee.last_day)))


"""creates a form for editing permanent employees that includes fields for the employee's 
name, address, and hourly pay rate, as well as their hire date and salary."""


class PermanentForm(HourlyForm):

    # def __init__(self, parent=None):
    #     super().__init__(parent)
    #     # self.file_path = file_path

    def fill_in(self, index):
        super().fill_in(index)
        self.layout.addRow(QLabel("Hired date: " + str(self._employee.hired_date)))


class AboutForm(QtWidgets.QWidget):
    """An About Form just gives information about our app to users who want to see it.  Automatically
    sets itself visible on creation."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("HR Management System"))
        self.layout.addWidget(QLabel("version 1.0.0"))
        self.layout.addWidget(QLabel("A simple system for storing important pieces of information about employees."))
        self.close = QPushButton("Close")
        self.close.clicked.connect(self.close_form)
        self.layout.addWidget(self.close)
        self.setLayout(self.layout)

    def close_form(self) -> None:
        """Hide the form."""
        self.setVisible(False)
