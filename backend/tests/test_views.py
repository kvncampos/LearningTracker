import pytest
from django.contrib.auth.models import User
from learningtracker.models import DailyLearning, Tag
from rest_framework import status
from rest_framework.test import APIClient


#################################################################
#                   WELCOME VIEW TEST
#################################################################
def test_welcome_view():
    """Test the WelcomeView endpoint."""
    client = APIClient()
    response = client.get("/")  # Assuming WelcomeView is mapped to "/"
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Welcome to the Learning Tracker API!"


#################################################################
#                   LOGIN VIEW TEST
#################################################################
# TODO ADD MISSING TESTS HERE.
#################################################################
#                   LOGOUT VIEW TEST
#################################################################
@pytest.mark.django_db
def test_logout_view():
    """Test the LogoutView endpoint."""
    # Step 1: Create a test user and log in
    user = User.objects.create_user(username="testuser", password="password")
    client = APIClient()
    client.force_authenticate(user=user)

    # Step 2: Perform logout request
    response = client.post("/api/logout/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Logged out successfully"


#################################################################
#                   DAILY LEARNING VIEWSET TESTS
#################################################################
@pytest.mark.django_db
def test_daily_learning_list(create_test_user):
    """Test listing daily learning entries for an authenticated user."""
    user = create_test_user
    DailyLearning.objects.create(
        user=user, date="2023-01-01", learning_type="Python", description="Test entry"
    )
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/learned-entries/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["description"] == "Test entry"


@pytest.mark.django_db
def test_daily_learning_create(create_test_user):
    """Test creating a daily learning entry."""
    user = create_test_user
    client = APIClient()
    client.force_authenticate(user=user)

    data = {
        "date": "2023-01-01",
        "learning_type": "Python",
        "description": "Learned about Python testing",
    }
    response = client.post("/api/learned-entries/", data=data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert DailyLearning.objects.filter(
        user=user, description=data["description"]
    ).exists()


@pytest.mark.django_db
def test_daily_learning_update(create_test_user):
    """Test updating a daily learning entry."""
    user = create_test_user
    entry = DailyLearning.objects.create(
        user=user, date="2023-01-01", learning_type="Python", description="Test entry"
    )
    client = APIClient()
    client.force_authenticate(user=user)

    updated_data = {
        "date": "2023-01-01",
        "learning_type": "Python",
        "description": "Updated entry",
    }
    response = client.put(
        f"/api/learned-entries/{entry.id}/", data=updated_data, format="json"
    )
    assert response.status_code == status.HTTP_200_OK
    entry.refresh_from_db()
    assert entry.description == "Updated entry"


#################################################################
#                   TAG VIEWSET TESTS
#################################################################
@pytest.mark.django_db
def test_tag_list(create_test_user):
    """Test listing tags for an authenticated user."""
    user = create_test_user
    Tag.objects.create(user=user, name="Python")
    Tag.objects.create(user=user, name="Django")
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/tags/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert response.json()[0]["name"] in ["Python", "Django"]


@pytest.mark.django_db
def test_tag_create(create_test_user):
    """Test creating a tag."""
    user = create_test_user
    client = APIClient()
    client.force_authenticate(user=user)

    data = {"name": "Python"}
    response = client.post("/api/tags/", data=data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Tag.objects.filter(user=user, name=data["name"]).exists()


@pytest.mark.django_db
def test_tag_update(create_test_user):
    """Test updating a tag."""
    user = create_test_user
    tag = Tag.objects.create(user=user, name="Python")
    client = APIClient()
    client.force_authenticate(user=user)

    updated_data = {"name": "Django"}
    response = client.put(f"/api/tags/{tag.id}/", data=updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    tag.refresh_from_db()
    assert tag.name == "Django"
