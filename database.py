from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# URL to create a location for the database on our fastAPI application
# DB is in this directory of our todo app
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:password@127.0.0.1:3306/TodoApplicationDatabase'


# create and engine to open up a db connection to use our database
# Connect Arguments passed to engine define connection to a db.  Only one thread will communicate with sql for independent requests
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# Create an instance of sessionLocal from sessionmaker, bind to the engine created do not auto commit or flush data
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create SQL DB  object that we can interact with
# Used to create database tables and interact with them
Base = declarative_base()
