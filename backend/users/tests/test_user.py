import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


def test_create_user_with_email_successfull():
    """
    Test creating a new user with email is successfull
    """
    email = "test@ultigu.com"
    password = "testpass12345!"

    user = User.objects.create_user(
        email=email,
        password=password
    )

    assert user.email == email
    assert user.check_password(password)


def test_new_user_email_normalized():
    """
    Test the email for a new user is normalized
    """
    email = "test@MARIO.de"
    password = "testpass12345!"
    user = User.objects.create_user(
        email=email,
        password=password
    )
    assert user.email == email.lower()


def test_new_user_invalid_email():
    """
    Test creating user with no email raises error
    """
    with pytest.raises(ValueError):
        User.objects.create_user(
            None,
            "123456"
        )


def test_create_new_superuser_with_pytest():
    """
    Test creating a new super user
    """
    user = User.objects.create_superuser(
        "test@mario.de",
        "123123"
    )
    assert user.is_superuser
    assert user.is_staff
