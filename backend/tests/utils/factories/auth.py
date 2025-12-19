import factory
from factory.alchemy import SQLAlchemyModelFactory
from ....models import Users, Todos
from faker import Faker
from passlib.context import CryptContext

fake = Faker()


# Use the same scheme as routers/auth.py
password_context = CryptContext(schemes=["argon2"], deprecated="auto")


class TodosFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Todos
        # Don't set session here - fixtures will handle session
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n + 1)
    title = factory.LazyFunction(lambda: fake.sentence(nb_words=4))
    description = factory.LazyFunction(lambda: fake.paragraph(nb_sentences=2))
    priority = factory.LazyFunction(lambda: fake.random_int(min=1, max=5))
    complete = False
    owner = None  # set by UserFactory


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Users
        # Don't set session here - fixtures will handle session
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n + 1)
    username = factory.LazyFunction(lambda: f"user{fake.random_int()}")
    email = factory.LazyFunction(lambda: f"user{fake.random_int()}@example.com")
    first_name = factory.LazyFunction(fake.first_name)
    last_name = factory.LazyFunction(fake.last_name)

    
# ✅ Hash a known plaintext here (do NOT define _plain_password as a field)
    hashed_password = factory.LazyAttribute(lambda o: password_context.hash("Password123!"))

    role = "user"
    is_active = True
    phone_number = None

    todos = factory.RelatedFactoryList(
        TodosFactory,
        factory_related_name="owner",
        size=0  # Default to 0, can be overridden with todos__size=N
    )