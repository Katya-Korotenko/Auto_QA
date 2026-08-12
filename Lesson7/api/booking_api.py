import requests

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