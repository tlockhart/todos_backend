from fastapi.testclient import TestClient # create a test client for our app
from ..main import app # import main file
from fastapi import status
# import models
# models.Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "Healthy"}
   
# def database import engine
#     response = client.get("/healthy")


