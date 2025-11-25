from fastapi import FastAPI
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users
from fastapi.middleware.cors import CORSMiddleware

""" 
Step 1 of 2: Include auth,py files from routers directory
"""

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
Base.metadata.create_all(bind=engine)

# Create Health Check route
@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)