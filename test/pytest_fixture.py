import pytest

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
@pytest.fixture
def student():
    return Student("Alice", 20)  # Created once, reused

def test_student_creation(student):
    assert student.name == "Alice"
    assert student.age == 20