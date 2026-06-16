import pytest
from django.contrib.auth import get_user_model
from core.models import PlatformUser


@pytest.mark.django_db
def test_create_platform_user():

    user = PlatformUser.objects.create(
        bale_user_id=123,
        username="testuser",
    )

    assert user.bale_user_id == 123
    assert user.username == "testuser"