import requests
import pytest

BASE_URL = "https://restful-booker.herokuapp.com"

DEFAULT_BOOKING = {
    "first_name": "Anna",
    "last_name": "Smith",
    "total_price": 150,
    "deposit_paid": True,
    "checkin": "2025-01-01",
    "checkout": "2025-01-05",
    "additional_needs": "Breakfast"
}


class BookingApi:
    def __init__(self, url):
        self.url = url

    def get_token(self):
        resp = requests.post(
            self.url + '/auth',
            json={"username": "admin", "password": "password123"}
        )
        assert resp.status_code == 200, f"Ожидался 200, получен {resp.status_code}"
        return resp.json()["token"]

    def create_booking(self, first_name, last_name, total_price,
                       deposit_paid, checkin, checkout, additional_needs=""):
        resp = requests.post(
            self.url + '/booking',
            json={
                "firstname": first_name,
                "lastname": last_name,
                "totalprice": total_price,
                "depositpaid": deposit_paid,
                "bookingdates": {"checkin": checkin, "checkout": checkout},
                "additionalneeds": additional_needs
            },
            headers={"Content-Type": "application/json"}
        )
        assert resp.status_code == 200, f"Ожидался 200, получен {resp.status_code}"
        return resp.json()

    def get_booking(self, booking_id):
        resp = requests.get(self.url + f'/booking/{booking_id}')
        assert resp.status_code == 200, f"Ожидался 200, получен {resp.status_code}"
        return resp.json()

    def partial_update_booking(self, booking_id, token, **kwargs):
        resp = requests.patch(
            self.url + f'/booking/{booking_id}',
            json=kwargs,
            headers={
                "Content-Type": "application/json",
                "Cookie": f"token={token}"
            }
        )
        assert resp.status_code == 200, f"Ожидался 200, получен {resp.status_code}"
        return resp.json()

    def get_booking_non_existing(self, booking_id):
        return requests.get(self.url + f'/booking/{booking_id}')


@pytest.fixture(scope="class")
def api():
    return BookingApi(BASE_URL)


class TestBookingApi:
    @pytest.fixture(scope="class", autouse=True)
    def setup(self, api, request):
        request.cls.api = api
        request.cls.token = api.get_token()

    def create_default_booking(self, **overrides):
        data = {**DEFAULT_BOOKING, **overrides}
        return self.api.create_booking(**data)

    # ——— Позитивные тесты ———

    @pytest.mark.positive
    @pytest.mark.parametrize("first_name, last_name, total_price", [
        ("Anna",  "Smith", 150),    # обычный случай
        ("John",  "Doe",   0),      # нулевая цена
        ("Maria", "Jones", 99999),  # максимальная цена
    ])
    def test_create_booking(self, first_name, last_name, total_price):
        result = self.create_default_booking(
            first_name=first_name,
            last_name=last_name,
            total_price=total_price
        )
        assert "bookingid" in result
        assert result["booking"]["firstname"] == first_name
        assert result["booking"]["lastname"] == last_name
        assert result["booking"]["totalprice"] == total_price

    @pytest.mark.positive
    def test_partial_update_booking(self):
        created = self.create_default_booking(
            first_name="John",
            last_name="Doe",
            total_price=100,
            deposit_paid=False
        )
        booking_id = created["bookingid"]

        updated = self.api.partial_update_booking(
            booking_id,
            self.token,
            firstname="Updated",
            totalprice=999
        )

        assert updated["firstname"] == "Updated"
        assert updated["totalprice"] == 999
        assert updated["lastname"] == "Doe"
        assert updated["depositpaid"] is False

    @pytest.mark.positive
    def test_get_booking_after_create(self):
        created = self.create_default_booking(
            first_name="Maria",
            last_name="Jones",
            total_price=200
        )
        booking = self.api.get_booking(created["bookingid"])

        assert booking["firstname"] == "Maria"
        assert booking["lastname"] == "Jones"
        assert booking["totalprice"] == 200

    # ——— Негативные тесты ———

    @pytest.mark.negative
    def test_get_non_existing_booking(self):
        resp = self.api.get_booking_non_existing(999999999)
        assert resp.status_code == 404, f"Ожидался 404, получен {resp.status_code}"

    @pytest.mark.negative
    def test_update_without_token(self):
        """Попытка обновить бронь без токена — должен вернуть 403"""
        created = self.create_default_booking()
        booking_id = created["bookingid"]

        resp = requests.patch(
            BASE_URL + f'/booking/{booking_id}',
            json={"firstname": "Hacker"},
            headers={"Content-Type": "application/json"}
        )
        assert resp.status_code == 403, f"Ожидался 403, получен {resp.status_code}"