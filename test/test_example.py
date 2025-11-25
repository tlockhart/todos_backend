import pytest

# One test
def test_equal_or_not_equal():
    # Two asserts that must pass in order for test to pass
    assert 1 + 1 == 2
    assert 2 * 2 != 5

def test_not_equal():
    assert 3 != 2

def test_is_instance():
    assert isinstance("this is a string", str)
    assert not isinstance("10", int)

def test_boolean():
    validated = True
    assert validated is True
    assert ('hello' == 'world') is False

def test_type():
    assert type('Hello') is str
    assert type('World') is not int

def test_greater_and_less_than():
    assert 5 > 3
    assert 2 < 4
    assert 10 >= 10
    assert 8 <= 12

def test_list():    
    num_list = [1, 2, 3, 4, 5]
    any_list = [False, False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)

class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years
@pytest.fixture
def default_employee():
    return Student("John", "Doe", "Computer Science", 3)

def test_person_initialization(default_employee):
    assert default_employee.first_name == "John"
    assert default_employee.last_name == "Doe"
    assert default_employee.major == "Computer Science"
    assert default_employee.years == 3

# def test_person_intialization():
#     student = Student("John", "Doe", "Computer Science", 3)
#     assert student.first_name == "John", "First name should be John"
#     assert student.last_name == "Doe", "Last name should be Doe"
#     assert student.major == "Computer Science"
#     assert student.years == 3