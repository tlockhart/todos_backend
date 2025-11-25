import pytest

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

def test_student_creation():
    student = Student("Alice", 20)
    assert student.name == "Alice"
    assert student.age == 20