import requests
import json

def run():
    url = "http://localhost:8000/api/token/"
    data = {
        "username": "admin",
        "password": "admin"
    }
    response = requests.post(
        url,
        data=data
    )

    user_token = response.json()

    print(user_token)

    url = "http://localhost:8000/api/item/"

    headers = {
        "Authorization": "Bearer {0}".format(user_token['access']),
        "Content-Type": 'application/json'
    }
    response = requests.get(
        url,
        headers=headers)
    print(response.json())

    url = "http://localhost:8000/api/order/"
    data = {
        "item": [
            {"name": 1, "quantity": 1},
            {"name": 2, "quantity": 3}
        ]
    }
    headers = {
        "Authorization": "Bearer {0}".format(user_token['access']),
        "Content-Type": 'application/json'
    }
    response = requests.post(
        url,
        data=json.dumps(data),
        headers=headers)

    print(response.status_code)
