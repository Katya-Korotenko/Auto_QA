import pytest
from api.booking_api import BookingApi

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture(scope="class")
def api():
    return BookingApi(BASE_URL)