import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from django.core.files import File
from unittest.mock import MagicMock

User = get_user_model()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def create_admin():
    return User.objects.create_superuser(
        email="admin@domain.com",
        password="testpass12!",
    )


@pytest.fixture
def create_test_user():
    def mixed_user(**params):
        new_user = mixer.blend(User, **params)
        return new_user
    return mixed_user
