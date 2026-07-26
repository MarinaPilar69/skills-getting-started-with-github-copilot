import copy
import pytest
from urllib.parse import quote
from httpx import AsyncClient
from httpx import ASGITransport

from src.app import app, activities


@pytest.mark.asyncio
async def test_get_activities():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert "Chess Club" in data


@pytest.mark.asyncio
async def test_signup_and_unregister():
    backup = copy.deepcopy(activities)
    activity_name = "Chess Club"
    email = "testuser@example.com"
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # sign up
            r = await ac.post(f"/activities/{quote(activity_name)}/signup", params={"email": email})
            assert r.status_code == 200
            assert email in activities[activity_name]["participants"]

            # unregister
            r2 = await ac.request("DELETE", f"/activities/{quote(activity_name)}/signup", params={"email": email})
            assert r2.status_code == 200
            assert email not in activities[activity_name]["participants"]
    finally:
        activities.clear()
        activities.update(backup)
