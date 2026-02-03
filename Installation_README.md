# pip3 list : see what is installed in global denpendencies
# mkdir fastApi
# python3 -m venv .venv : setup venv mac
# MAC: source .venv/bin/activate : ###activate virtual environment####
# Windows (powershell): .venv\Scripts\Activate.ps1
# Windows (cmd): .venv/bin/activate.bat
# powershell: .venv\Scripts\Activate.ps1
# pip list : What is inside pip env
# deactivate : deactivate venv
# pip install fastapi "uvicorn[standard]" : install dependencies: 
# pip install "fastapi[standard]" : install fastapi[standard]
# pip install "passlib[bcrypt]" : install passlib
# pip install bcrypt==4.0.1 : alternative bcrypt passlib install
# pip install argon2_cffi : extend bcrypt password limit to greater than 72
# pip install "python-jose[cryptography]" : install jose
# pip install python-multipart : install multipart to submit forms to application, for token
# pip install sqlite3 (pysqlite3) : install sqllite
# pip install python-dotenv : install .env
# pip install sqlalchemy: Install SQLAchemy ORM in project:
# Windows: (Check version of install): python -m poetry --version
# WIndows: (IAC): (.venv) python -m hostmaster_iac_dev.main
# Windows: (IAC): (.venv): python = ">=3.11,<3.14"
# Windows: (IAC): Run hostmaster: python -m poetry run hostmaster-iac-dev
# Windows: (FRONTEND): python -m poetry run hostmaster-frontend-dev
# Windows: (BACKEND): python -m poetry run hostmaster-backend-dev
# pip freeze > requirements.txt : create dependencies file
# pip install -r requirements.txt --no-user, Load requirements
# openssl rand -hex 32 : generate a secret key
# brew list : check if sqllite installed for mac
# brew install sqlite : install if not already installed
# xattr -c todosapp.db : remove readonly db permission
# sqlite3 : run sqlite3
# .quit : stop sqlite3
# sqlite3 todosapp.db : start db
# .schema : check tables
# insert into todos(title, description, priority, complete) values ('Go to the store', 'Pick up eggs', 5, False);
# select * from todos;
# .mode column (markdown, box, table) : select column view
# delete from todos where id = 4; : delete element

# open fastAPI, create new file books.py
# [OPTION 1: run fastAPI ]  : uvicorn books:app --reload
uvicorn main:app --reload
# [OPTION 2: run fastAPI ] :  fastapi run books.py 
# [OPTION 3: run dav fastAPI ] : fastapi dev books.py
## uvicorn is the server

# http://127.0.0.1:8000/docs : open swagger api endpoints

# %20 : Space between path parameters
# casefold : lowercase

# Add todo:
# 1|Learn FastAPI|Because it's awesome|5|0|1
# 2|Learn FastAPI|Because it's awesome|5|0|1

# PostgreSQL (Pgadmin4)
# pip install psycopg2-binary :  install postgress connection
## https://www.pgadmin.org/download/pgadmin-4-macos/
# Commands:
## sudo mkdir -p /etc/paths.d &&
## echo /Applications/Postgres.app/Contents/Versions/latest/bin | sudo tee /etc/paths.d/postgresapp
## Password: password
## Sign in user: codingwithroby, pw: password
"""
✅ Fix in pgAdmin 4
	1.	Right-click → Create → Database
In pgAdmin, when you create a database, the Template defaults to template1.
	2.	Change Template to template0
	•	In the Create Database dialog, go to the Definition tab.
	•	Find Template and set it to template0.
	•	Save.
This avoids the mismatch because template0 is a barebones template.
""" 

# Mysql Community Edition installation (mysql workbench):
## https://dev.mysql.com/downloads/file/?id=544297
## pip install pymysql : install mysql

# Install Alembic:
## pip install alembic : install alembic
## alembic init <folder name: alembic> : Initialize a new, generic environment
### Update database url in alembic.ini file: sqlalchemy.url = driver://user:pass@localhost/dbname
## Terminal: alembic revision -m <"create phone number col on users table" : message> : create a new revision of the environment
## alembic upgrade <revision #> : Run our upgrade migration to our database
### Version: def upgrade() -> None: op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
### Terminal: python -m alembic upgrade revision id 
### Example: python -m alembic upgrade 853fc1cecec8
## alembic downgrade -1 : Run our downgrade migration to our database
### Version: def downgrade() -> None: op.drop_column('users', 'phone_number')
### Terminal: python -m alembic downgrade -1

## TEst your connection from project (fastAPI):
### Start postgress db: Get-Service -Name "*postgres*"
### Open mySQL Program
### Click Start MySQL Server
### FASTAPI is the project
### First activate .venv from fastAPI project
### source .venv/bin/activate
### run Application from package: uvicorn todos_backend.main:app --reload
### You should be able to reach: http://127.0.0.1:8000/healthy
# Disable warnings:
## pytest --disable-warnings: hide pytest warnings

# Test Commands:
## pytest -v : verbose


# Pytests: Run from backend
## from todos_backend package run commands:
### pytest -v --tb=short tests/unit/test_user_unit.py
### pytest -v --tb=short tests/unit/test_todos_unit.py
### pytest -v --tb=short tests/integration/test_user_integration.py
### START MySQL
#### pytest -v --tb=short tests/integration/test_todos_integration.py

### pytest -v --tb=short tests/integration/test_todos_with_factory_update.py
### pytest -v --tb=short tests/unit/test_users_with_factory_update.py
### pytest -v --tb=short tests/integration/test_admin.py
### pytest -v --tb=short tests/unit/test_user_model.unit.py

### Install python Symantec Release:
## py -3 -m pip install --upgrade pip
## py -3 -m pip install python-semantic-release
## py -3 -m semantic_release --help
### Then run the command via the module name:
## py -3 -m semantic_release generate-config
## python -m pip install -U python-semantic-release --no-user
### Generate .toml
## python -m semantic_release generate-config
## python -m semantic_release generate-config --pyproject >> pyproject.toml

### Install Dependencies
## python -m pip install -U pip setuptools wheel build python-semantic-release --no-user

### Create Change log:
## python -m semantic_release publish

### Append to Change Log:
## python -m semantic_release changelog

### Add __version__="0.0.0" to backend/__init__.py
### backend/__init__.py

### Update Changelog:
## python -m semantic_release changelog

### Run safe trial semantic release
## python -m semantic_release version --no-push


### Remove user requirement:
## python -m pip config list -v
