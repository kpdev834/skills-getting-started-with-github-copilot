import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test GET /activities

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"], dict)

# Test POST /activities/{activity_name}/signup

def test_signup_for_activity():
    activity = "Art Club"
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Try signing up again (should fail)
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

# Test DELETE /activities/{activity_name}/unregister

def test_unregister_from_activity():
    activity = "Art Club"
    email = "newstudent@mergington.edu"
    # Unregister the student
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"
    # Try unregistering again (should fail)
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"

# Test signup for non-existent activity

def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup", params={"email": "student@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

# Test unregister for non-existent activity

def test_unregister_nonexistent_activity():
    response = client.delete("/activities/Nonexistent/unregister", params={"email": "student@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
