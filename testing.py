import requests
from time import sleep
import json

def check_status():
    status_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/status/"
    status_headers = {"Content-Type": "application/json",
                      "Authorization": f"Token 5740acca65a9d61760e99fb06308fe18cbf29a3c"}
    status_response = json.loads(requests.post(
        status_endpoint, headers=status_headers).content)
    sleep(status_response['cooldown'])
    return status_response

def get_init_response():
    init_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/init"
    init_headers = {
        "Authorization": f"Token 5740acca65a9d61760e99fb06308fe18cbf29a3c"}
    init_response = json.loads(requests.get(
        init_endpoint, headers=init_headers).content)
    sleep(init_response['cooldown'])
    return init_response

def examine_item(item):
    examine_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/"
    examine_headers = {"Content-Type": "application/json",
                       "Authorization": f"Token 5740acca65a9d61760e99fb06308fe18cbf29a3c"}
    examine_payload = {"name": item}
    examine_response = json.loads(requests.post(examine_endpoint, data=json.dumps(
        examine_payload), headers=examine_headers).content)
    sleep(examine_response['cooldown'])
    return examine_response

print(get_init_response())
print(check_status())
print(examine_item("WELL"))