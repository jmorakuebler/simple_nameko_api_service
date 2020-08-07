import json
import requests


headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
base_url = "http://localhost:8000"


def send_request(endpoint, method, payload):
    url = base_url+endpoint
    print('Sending request {} ..'.format(url))
    response = requests.request(method, base_url+endpoint, data=json.dumps(payload), headers=headers)
    print("Reponse received: ", response.text)
    print("\n")


# ENDPOINT /hello_world
send_request("/hello_world", "GET", {})

# ENDPOINT /greet_user
send_request("/greet_user/mark", "GET", {})

# ENDPOINT /create_user
payload = {'username': 'mark'}
send_request("/create_user", "POST", payload)
