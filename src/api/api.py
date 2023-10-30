import requests
import json

## API Request
def request(url, headers, params=None, data=None, debug = False):
    if data is None:
        if debug: print("GET request: ", url, "\n\tParams: ", params)
        response = requests.get(url, params=params, headers=headers)
    else:
        if debug: print("POST request: ", url, "\n\tParams: ", params, "\n\tData: ", data)
        response = requests.post(url, params=params, data=json.dumps(data), headers=headers)

    if debug: print("\tResponse: ", response.json())

    if response.status_code == 200:
        return response.json()
    else:
        return response.raise_for_status()