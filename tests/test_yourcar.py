import pytest

from yourcar import YourCarAPIClient, Place

LAT_ROSTOCK = 54.0833
LON_ROSTOCK = 12.1333


@pytest.fixture
def api_key():
    import os

    return os.environ.get("YOURCAR_API_KEY", "YEK-IPA")


@pytest.fixture
def client(api_key):
    return YourCarAPIClient(api_key)


@pytest.fixture(scope="module", autouse=True)
def vcr_config():
    return {"filter_headers": [("X-API-KEY", "DUMMY_API_KEY")]}


@pytest.mark.vcr()
def test_places_successful(client):
    """Tests an API call to get places near a location in a given range"""
    places = client.places(lat=LAT_ROSTOCK, lon=LON_ROSTOCK, distance=2000)

    assert isinstance(places, list)
    assert len(places) == 15

    first = places[0]
    assert isinstance(first, Place)
    assert first.id == "4402"
    assert first.name == "August-Bebel-Str. 71"
    assert first.geo_position.latitude == 54.085047
    assert first.geo_position.longitude == 12.133862
    assert first.distance - 197.9 < 0.1
