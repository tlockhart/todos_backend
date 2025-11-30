from fastapi import status
from fastapi.testclient import TestClient
from ..main import app
from ..models import Todos

from ..utils.database.connection import get_db_session, get_current_user
from .utils import override_get_db_session, override_get_current_user, TestingSessionLocal
app.dependency_overrides[get_db_session] = override_get_db_session
app.dependency_overrides[get_current_user] = override_get_current_user


client = TestClient(app)

def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == 200
    assert response.json() == [
        {
            'complete': False, 'title': 'Learn to code!',
            'description': 'Need to learn everyday!',
            'priority': 5, 'owner_id': 1, 'id': 1
        }
    ]   

def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == 200
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None
      
def test_admin_delete_todo_not_found(test_todo):
    response = client.delete("/admin/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}