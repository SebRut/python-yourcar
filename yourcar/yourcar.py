import requests
import json
import jsons
from jsons import KEY_TRANSFORMER_SNAKECASE
from dataclasses import dataclass
import datetime
from typing import List

BASE_URL = "https://de1.cantamen.de/casirest/v2/"


@dataclass
class Coord:
    latitude: float
    longitude: float


@dataclass
class Place:
    id: str
    name: str
    geo_position: Coord
    distance: float


class YourCarAPIClient(object):
    def __init__(self, api_key: str):
        """
        :type api_key: The API key to be used
        """

        self._session = requests.Session()
        self._session.headers = {"X-API-KEY": api_key}

    def places(
        self, lat: float, lon: float, distance: int, rental_start: datetime = None
    ) -> List[Place]:
        params = {"lat": lat, "lng": lon, "range": distance}

        if rental_start:
            params["start"] = rental_start.isoformat()

        resp = self._get("places", params)
        parsed_json = json.loads(resp.text)
        return [
            jsons.load(item, Place, key_transformer=KEY_TRANSFORMER_SNAKECASE)
            for item in parsed_json
        ]

    def _get(self, resource: str, params=None) -> requests.Response:
        url = BASE_URL + resource
        response = self._session.get(url, params=params)

        if response.status_code != 200:
            response.raise_for_status()

        return response
