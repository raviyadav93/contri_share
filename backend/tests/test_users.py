"""Tests for user endpoints."""
import pytest
from app.schemas.user import UserCreate


def test_create_user(client):
    """Test user creation."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "test_password_123"
    }
    response = client.post("/api/v1/users", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "id" in data


def test_get_user(client):
    """Test getting a user."""
    # First create a user
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "test_password_123"
    }
    create_response = client.post("/api/v1/users", json=user_data)
    user_id = create_response.json()["id"]
    
    # Then get the user
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == user_data["email"]


def test_user_not_found(client):
    """Test getting non-existent user."""
    response = client.get("/api/v1/users/999")
    assert response.status_code == 404
