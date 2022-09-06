import pytest
from main import app
from application.data.database import db
from application.data.models import User, Tracker, TrackerLog
from json import loads, dumps
from bs4 import BeautifulSoup

USER_URL = "http://localhost:8000"
EMAIL = "testing123@gmail.com"
PASSWORD = "12345678"
AUTH_TOKEN = ""
DATA = {
    "email": EMAIL,
    "password": PASSWORD
}
HEADER = {
    "Content-Type": "application/json"
}


def test_register(client, init_database):
    URL = USER_URL + "/register"
    response = client.post(URL, json=DATA)

    # print(response.data)

def test_login(client, init_database):
    url = USER_URL + "/logout"
    response = client.post(url)

    url = USER_URL + "/login?include_auth_token"
    response = client.post(url, json=DATA)

    AUTH_TOKEN = loads(response.data)["response"]["user"]["authentication_token"]
    HEADER["Authentication-Token"] = AUTH_TOKEN


def test_get_1(client, init_database):
    """
    Test for GET API.
    GOAL - Provide wrong authentication token
    """
    url = USER_URL + "/api/user"

    response = client.get(url, headers={
        "Content-Type": "application/json",
        "Authentication-Token": ""
    })

    assert response.status_code == 401

def test_get_2(client, init_database):
    """
    Test for GET API.
    GOAL - Provide correct authentication token
    """
    url = USER_URL + "/api/user"

    response = client.get(url, headers=HEADER)

    assert response.status_code == 200


def test_put_1(client, init_database):
    """
    Test for PUT API.
    GOAL - Provide wrong email id
    """
    url = USER_URL + "/api/user"

    data = {
        "email": ""
    }

    response = client.put(url, headers=HEADER, json=data)

    assert response.status_code == 400

def test_put_2(client, init_database):
    """
    Test for PUT API.
    GOAL - Provide duplicate email id
    """
    url = USER_URL + "/api/user"

    data = {
        "email": "testing123@gmail.com"
    }

    response = client.put(url, headers=HEADER, json=data)

    assert response.status_code == 400

def test_put_3(client, init_database):
    """
    Test for PUT API.
    GOAL - Provide correct email id
    """
    url = USER_URL + "/api/user"

    data = {
        "email": "qwerty@gmail.com"
    }

    response = client.put(url, headers=HEADER, json=data)

    assert response.status_code == 200


def test_delete_1(client, init_database):
    """
    Test for DELETE API
    """
    url = USER_URL + "/api/user"

    response = client.delete(url, headers=HEADER)

    assert response.status_code == 200