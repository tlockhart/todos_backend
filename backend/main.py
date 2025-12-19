from fastapi import FastAPI
from .models import Base
from .utils.database.connection import engine
from .routers import auth, todos, admin, users
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

""" 
Step 1 of 2: Include auth,py files from routers directory
"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create a new todoapp db From database/engine
    # Only ran if todos.db does not exist
    Base.metadata.create_all(bind=engine)
    yield

# Root folder uses our fastAPI Application
app = FastAPI(lifespan=lifespan)

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

# Create Health Check route
@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)