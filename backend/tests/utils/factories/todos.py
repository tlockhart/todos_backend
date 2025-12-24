import factory
# DJANGO SUBSTITUTION: from factory.django import DjangoModelFactory
from factory.alchemy import SQLAlchemyModelFactory
from ....models import Todos
from faker import Faker
from .auth import UserFactory

fake = Faker()


# DJANGO SUBSTITUTION: class TodosFactory(DjangoModelFactory):
class TodosFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Todos
        # DJANGO SUBSTITUTION: Remove sqlalchemy_session lines. Django uses the default DB connection automatically.
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
# DJANGO SUBSTITUTION: This pattern works in Django too, but ensure 'owner' matches the field name in your Django model.
UserFactory.todos = factory.RelatedFactoryList(
    TodosFactory,
    factory_related_name="owner",
    size=0,  # Default to 0, can be overridden with todos__size=N
)
