from requests import request
import json
import datetime

API_URL = "http://api.cup2022.ir/api/v1"


def register(name, email, password):
    url = f"{API_URL}/user"
    payload = json.dumps(
        {
            "name": name,
            "email": email,
            "password": password,
            "passwordConfirm": password,
        }
    )

    headers = {"Content-Type": "application/json"}

    response = request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)


def login(email, password):
    url = f"{API_URL}/user/login"
    payload = json.dumps(
        {
            "email": email,
            "password": password,
        }
    )

    headers = {"Content-Type": "application/json"}

    response = request("POST", url, headers=headers, data=payload)

    return json.loads(response.text).get("data", {}).get("token", "")


def teams(token):
    url = f"{API_URL}/team"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    response = request("GET", url, headers=headers)

    return json.loads(response.text)


def teams_per_id(token, id):
    url = f"{API_URL}/team/{id}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    response = request("GET", url, headers=headers)

    return json.loads(response.text)


def standings_by_group(token, group):
    url = f"{API_URL}/standings/{group}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    response = request("GET", url, headers=headers)

    return json.loads(response.text)


def matches_today(token):
    url = f"{API_URL}/bydate"
    payload = json.dumps(
        {"date": f"{datetime.datetime.today().date().strftime('%m/%d/%Y')}"}
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    response = request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)
