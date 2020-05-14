from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


def test_user_page_status(create_admin):
    """
    Test user are listed on user page
    """
    client = Client()
    client.force_login(create_admin)
    url = reverse("admin:users_user_changelist")
    res = client.get(url)
    assert res.status_code == 200, 'Should give the Status Code 200'


def test_user_change_page(create_admin, create_test_user):
    """
    Test that the user edit page works
    """
    client = Client()
    client.force_login(create_admin)
    user = create_test_user()
    url = reverse("admin:users_user_change", args=[user.id])
    res = client.get(url)

    assert res.status_code == 200, 'Should give the Status Code 200'


def test_create_user_page(create_admin):
    """
    Test that the create user page works
    """
    client = Client()
    client.force_login(create_admin)
    url = reverse("admin:users_user_add")
    res = client.get(url)

    assert res.status_code == 200, 'Should give the Status Code 200'
