import pytest
import random
from core.models import PlatformUser


@pytest.fixture
async def user():
    return await PlatformUser.objects.acreate(
        bale_user_id=random.randint(10000, 99999),
        username="tester",
    )