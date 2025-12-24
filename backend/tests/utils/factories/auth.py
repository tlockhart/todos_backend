import factory
from factory.alchemy import SQLAlchemyModelFactory
from ....models import Users
from faker import Faker
from passlib.context import CryptContext

fake = Faker()


# Use the same scheme as routers/auth.py
password_context = CryptContext(schemes=["argon2"], deprecated="auto")


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Users
        # Don't set session here - fixtures will handle session
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    """Using factory.Sequence explicitly sets the id 
    for every instance starting from 1. In a persistent 
    test database (or across multiple tests), this will 
    quickly collide with existing rows, causing the UNIQUE 
    constraint failed: users.id error you’re seeing."""
    # NEVER SET THE ID
    # id = factory.Sequence(lambda n: n + 1)
    username = factory.LazyFunction(lambda: f"user{fake.random_int()}")
    email = factory.LazyFunction(lambda: f"user{fake.random_int()}@example.com")
    first_name = factory.LazyFunction(fake.first_name)
    last_name = factory.LazyFunction(fake.last_name)

    # ✅ Hash a known plaintext here (do NOT define _plain_password as a field)
    hashed_password = factory.LazyAttribute(
        lambda o: password_context.hash("Password123!")
    )

    role = "admin"
    is_active = True
    phone_number = None
