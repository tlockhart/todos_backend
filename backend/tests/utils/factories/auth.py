import factory
from factory.alchemy import SQLAlchemyModelFactory
from backend.models import User, Todos
from faker import Faker
from backend.utils.database.connection import get_db_session

# Helper: get a real session from the generator safely
def get_factory_session():
    gen = get_db_session()  # returns a generator
    session = next(gen)
    return session

factory_session = get_factory_session()
fake = Faker()

class TodosFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Todos
        sqlalchemy_session = factory_session
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n + 1)
    title = factory.LazyFunction(lambda: fake.sentence(nb_words=4))
    description = factory.LazyFunction(lambda: fake.paragraph(nb_sentences=2))
    priority = factory.LazyFunction(lambda: fake.random_int(min=1, max=5))
    complete = False
    owner = None  # set by UserFactory


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = factory_session
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n + 1)
    username = factory.LazyFunction(lambda: f"user{fake.random_int()}")
    email = factory.LazyFunction(lambda: f"user{fake.random_int()}@example.com")
    first_name = factory.LazyFunction(fake.first_name)
    last_name = factory.LazyFunction(fake.last_name)
    hashed_password = factory.LazyFunction(fake.password)
    role = "user"
    is_active = True
    phone_number = None

    todos = factory.RelatedFactoryList(
        TodosFactory,
        factory_related_name="owner",
        size=3
    )