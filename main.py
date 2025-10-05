from fastapi import FastAPI
import models
from database import engine

""" 
Step 1 of 2: Include auth,py files from routers directory
"""
from routers import auth, todos, admin, users

from fastapi.middleware.cors import CORSMiddleware

# Root folder uses our fastAPI Application
app = FastAPI()

# Allow requests from your frontend
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Allow listed origins
    allow_credentials=True,
    allow_methods=["*"],            # Allow all HTTP methods
    allow_headers=["*"],            # Allow all headers
)

# Create a new todoapp db From database/engine
# Only ran if todos.db does not exist
models.Base.metadata.create_all(bind=engine)

    
"""
Step 2 of 2: INCLUDE API Inputs from ROUTERS
"""
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)