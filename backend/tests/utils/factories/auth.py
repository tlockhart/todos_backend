import factory
from factory.alchemy import SQLAlchemyModelFactory
from ....models import Users, Todos
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


class TodosFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Todos
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
    title = factory.LazyFunction(lambda: fake.sentence(nb_words=4))
    description = factory.LazyFunction(lambda: fake.paragraph(nb_sentences=2))
    priority = factory.LazyFunction(lambda: fake.random_int(min=1, max=5))
    complete = False
    owner = factory.SubFactory(UserFactory)


# Circular dependency resolution: Define todos after TodosFactory is created
UserFactory.todos = factory.RelatedFactoryList(
    TodosFactory,
    factory_related_name="owner",
    size=0,  # Default to 0, can be overridden with todos__size=N
)
