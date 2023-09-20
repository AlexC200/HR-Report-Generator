""" Employee .py file inputting info for the gui"""

from enum import Enum
import abc
from datetime import date
from datetime import datetime

"""Enumerated list for Employee's positions in company"""


class Role(Enum):
    CEO = 1
    CFO = 2
    COO = 3


"""Enumerated list for employee positions as "managers" """


class Department(Enum):
    ACCOUNTING = 1
    FINANCE = 2
    HR = 3
    R_AND_D = 4
    MACHINING = 5


"""Defines custom erorr types that can be used to raise errors with Role & Department"""


class InvalidRoleException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidDepartmentException(Exception):
    def __init__(self, message):
        super().__init__(message)


"""Provides a base class for defining employees with common attributes and methods, 
while allowing subclasses to provide their own implementations of the calc_pay() method."""


class Employee(abc.ABC):
    id_number = 0
    IMAGE_PLACEHOLDER = "./images/placeholder.png"

    def __init__(self, name: str, email: str):
        self.id_number = Employee.id_number
        Employee.id_number += 1
        self.name = name
        self.email = email
        self.image = Employee.IMAGE_PLACEHOLDER

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("Name cannot be blank")
        self._name = name

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if not email:
            raise ValueError("Email cannot be blank")
        if "@acme-machining.com" not in email:
            raise ValueError("Email must be from @acme-machining.com")
        self._email = email

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        if not image:
            raise ValueError("Image cannot be empty.")
        self._image = image

    def __repr__(self):
        return f"{self.name}, {self.email}, {self.image}"

    @abc.abstractmethod
    def calc_pay(self) -> float:
        pass

        """This function calculates the weekly pay for the current
        employee for our pay report."""


"""Defines a class Salaried that inherits from a parent class Employee. 
The Salaried class has an initializer method that takes three arguments: name, email, and yearly, 
and sets the name and email attributes using the initializer method of the parent class, 
and the yearly attribute using the provided yearly argument."""


class Salaried(Employee):
    def __init__(self, name: str, email: str, yearly: float):
        super().__init__(name, email)
        self.yearly = yearly

    @property
    def yearly(self):
        return self._yearly

    @yearly.setter
    def yearly(self, yearly):
        if yearly < 50000:
            raise ValueError("Yearly salary must be over $50,000")
        self._yearly = yearly

    def calc_pay(self):
        return self.yearly / 52.0

    def __repr__(self):
        base_repr = super().__repr__()
        return f"{base_repr}, {self.yearly}"


"""Essentially does the same as the above class and methods, except with hourly employee's"""


class Hourly(Employee):
    def __init__(self, name: str, email: str, hourly_wage: float):
        super().__init__(name, email)
        self.hourly_wage = hourly_wage

    @property
    def hourly_wage(self):
        return self._hourly_wage

    @hourly_wage.setter
    def hourly_wage(self, hourly_wage):
        if hourly_wage < 15 or hourly_wage > 99.99:
            raise ValueError("Hourly wage must be between $15 and $99.99 (inclusive)")
        self._hourly_wage = hourly_wage

    def calc_pay(self):
        return self.hourly_wage * 40.0

    def __repr__(self):
        base_repr = super().__repr__()
        return f"{base_repr},{self.hourly_wage}"


"""The code defines three subclasses of Employee: Executive, Manager, Permanent, and Temporary. 
Each subclass has its own specific attributes and behaviors inherited from 
the Employee class and its parent classes. The code also includes some input validation for certain attributes, 
such as checking the validity of the role and department values."""


class Executive(Salaried):

    def __init__(self, name: str, email: str, yearly: float, role: int):
        super().__init__(name, email, yearly)
        if role not in [s.value for s in Role]:
            raise InvalidRoleException(f"{role} is not a valid role.")
        self.role = Role(role)

    def __repr__(self):
        base_repr = super().__repr__()
        return f"{base_repr},{self.role.name}"


class Manager(Salaried):
    def __init__(self, name: str, email: str, yearly: float, department: Department):
        super().__init__(name, email, yearly)
        if department not in [d.value for d in Department]:
            raise InvalidDepartmentException(f"{department} is not a valid department.")
        self.department = Department(department)

    def __repr__(self):
        base_repr = super().__repr__()
        return f"{base_repr},{self.department.name}"


class Permanent(Hourly):
    def __init__(self, name: str, email: str, hourly_wage: float, hired_date: datetime):
        super().__init__(name, email, hourly_wage)
        self.hired_date = hired_date

    def __repr__(self):
        base_repr = super().__repr__()
        return f"{base_repr},{self.hired_date}"


class Temporary(Hourly):
    def __init__(self, name: str, email: str, hourly_wage: float, last_day: date):
        super().__init__(name, email, hourly_wage)
        self.last_day = last_day

    def __repr__(self):
        base_repr = super().__repr__()
        return f"{base_repr}, {self.last_day}"
