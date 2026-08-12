import requests
import pytest
from test_data import DEFAULT_BOOKING

BASE_URL = "https://restful-booker.herokuapp.com"

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
        ("Anna",  "Smith", 150),
        ("John",  "Doe",   0),
        ("Maria", "Jones", 99999),
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
        resp = self.api.get_booking_non_existing(99999)
        assert resp.status_code == 404, f"Ожидался 404, получен {resp.status_code}"

    @pytest.mark.negative
    def test_update_without_token(self):
        created = self.create_default_booking()
        booking_id = created["bookingid"]

        resp = requests.patch(
            BASE_URL + f'/booking/{booking_id}',
            json={"firstname": "Smith"},
            headers={"Content-Type": "application/json"}
        )
        assert resp.status_code == 403, f"Ожидался 403, получен {resp.status_code}"