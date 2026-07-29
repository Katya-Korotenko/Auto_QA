import requests
import pytest

BASE_URL = "http://5.101.50.27:8000"


class EmployeeApi:
    def __init__(self, url):
        self.url = url

    def get_token(self, user, password):

        creds = {"username": user, "password": password}
        resp = requests.post(self.url + '/auth/login', json=creds)
        assert resp.status_code == 200
        return resp.json()["user_token"]

    def create_employee(self, first_name, last_name, company_id, user, password):

        token = self.get_token(user, password)
        resp = requests.post(
            self.url + f'/employee/create?client_token={token}',
            json={
                "first_name": first_name,
                "last_name": last_name,
                "companyId": company_id,
                "is_active": True
            }
        )
        assert resp.status_code == 201, f"Ожидался 201, получен {resp.status_code}"
        return resp.json()

    def get_employee(self, employee_id):

        resp = requests.get(
            self.url + '/employee/info',
            params={"id": employee_id}
        )
        return resp.json()

    def update_employee(self, employee_id, user, password, **kwargs):

        token = self.get_token(user, password)
        resp = requests.patch(
            self.url + f'/employee/change?client_token={token}',
            json={"id": employee_id, **kwargs}
        )
        assert resp.status_code == 200, f"Ожидался 200, получен {resp.status_code}"
        return resp.json()


# ——— Фикстура ———

@pytest.fixture
def api():
    return EmployeeApi(BASE_URL)


# ——— Тесты (по аналогии с test_company.py) ———

USER = "harrypotter"
PASS = "expelliarmus"

def test_create_employee(api):

    result = api.create_employee("Anna", "Smith", 1, USER, PASS)
    employee_id = result["id"]

    employee = api.get_employee(employee_id)
    assert employee["first_name"] == "Anna"
    assert employee["last_name"] == "Smith"
    assert employee["is_active"] is True

def test_update_employee(api):

    result = api.create_employee("Anna", "Smith", 1, USER, PASS)
    employee_id = result["id"]

    updated = api.update_employee(employee_id, USER, PASS, first_name="Updated")
    assert updated["first_name"] == "Updated"