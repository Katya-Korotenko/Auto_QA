import requests
import pytest

BASE_URL = "https://restful-booker.herokuapp.com"


# ——— API класс ———

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
                "bookingdates": {
                    "checkin": checkin,
                    "checkout": checkout
                },
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
        resp = requests.get(self.url + f'/booking/{booking_id}')
        return resp


# ——— Фикстура ———

@pytest.fixture(scope="class")
def api():
    return BookingApi(BASE_URL)


# ——— Тестовый класс ———

class TestBookingApi:
    @pytest.fixture(scope="class", autouse=True)
    def setup(self, api, request):
        request.cls.api = api
        request.cls.token = api.get_token()

    def test_create_booking(self):
        result = self.api.create_booking(
            first_name="Anna",
            last_name="Smith",
            total_price=150,
            deposit_paid=True,
            checkin="2025-01-01",
            checkout="2025-01-05",
            additional_needs="Breakfast"
        )

        assert "bookingid" in result, "В ответе нет bookingid"
        booking = result["booking"]
        assert booking["firstname"] == "Anna"
        assert booking["lastname"] == "Smith"
        assert booking["totalprice"] == 150
        assert booking["depositpaid"] is True
        assert booking["bookingdates"]["checkin"] == "2025-01-01"
        assert booking["bookingdates"]["checkout"] == "2025-01-05"
        assert booking["additionalneeds"] == "Breakfast"

    def test_partial_update_booking(self):
        created = self.api.create_booking(
            first_name="John",
            last_name="Doe",
            total_price=100,
            deposit_paid=False,
            checkin="2025-02-01",
            checkout="2025-02-05"
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
        # Остальные поля не должны измениться
        assert updated["lastname"] == "Doe"
        assert updated["depositpaid"] is False

    def test_get_booking_after_create(self):
        created = self.api.create_booking(
            first_name="Maria",
            last_name="Jones",
            total_price=200,
            deposit_paid=True,
            checkin="2025-03-01",
            checkout="2025-03-10"
        )
        booking_id = created["bookingid"]

        booking = self.api.get_booking(booking_id)
        assert booking["firstname"] == "Maria"
        assert booking["lastname"] == "Jones"
        assert booking["totalprice"] == 200

    def test_get_non_existing_booking(self):
        resp = self.api.get_booking_non_existing(999999999)
        assert resp.status_code == 404, f"Ожидался 404, получен {resp.status_code}"