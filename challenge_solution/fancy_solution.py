import logging
from typing import Any, Dict, Optional
import requests
from requests import Response

BASE_URL = "http://localhost:8000/challenge"


def check_status_response(response: Response) -> Response:
    if response.status_code == 401:
        raise PermissionError("Unauthorized")

    if response.status_code != 200:
        raise Exception(response.content)

    return response


def make_get_request(url: str, params: Optional[Dict[str, Any]] = None) -> Response:
    response = requests.get(BASE_URL + url, params=params)
    return check_status_response(response)


def make_post_request(url: str, json: Dict[str, Any]) -> Response:
    response = requests.post(BASE_URL + url, json=json)
    return check_status_response(response)


def main() -> None:
    # Get key
    key_result = make_get_request("/key")
    key = key_result.json()["key"]
    print("Getting key: ", key)

    # Get letter
    box_result = make_get_request("/box", params={"box_key": key})
    letter = box_result.text  # the response here is not a json, but a plain text
    print("Getting letter: ", letter)

    # Get child's feedback
    child_result = make_post_request("/child", json={"story": letter})
    room_code = child_result.json()["room_code"]  # The "feedback" field is only some text, we don't need it
    print("Getting room code: ", room_code)

    # Get vaults
    room_result = make_get_request("/room", params={"room_code": room_code})
    vaults = room_result.json()
    print(f"Getting vaults: {len(vaults)} vaults")

    for vault in vaults:
        # Get vault's content
        vault_result = make_post_request("/vault", json={"name": vault["name"], "password": vault["password"]})
        content = vault_result.json()["content"]

        if content:
            print(f"GIFT CARD found in the {vault['name']}:", content)
            break  # Gift card found, no need to continue


if __name__ == "__main__":
    try:
        try:
            main()
        except PermissionError as permission_error:
            print("Permission denied, trying again...")
            main()
    except Exception as error:
        print("Something went wrong:", error)
