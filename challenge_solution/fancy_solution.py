import logging
from typing import Any, Dict, Optional
import requests
from requests import Response

BASE_URL = "https://challenge.ivanbicalho.com"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    logger.info("Getting key...")
    key_result = make_get_request("/key")
    key = key_result.json()["key"]
    logger.info("Key: %s", key)

    # Get letter
    logger.info("Opening the box...")
    box_result = make_get_request("/box", params={"box_key": key})
    letter = box_result.text  # The response here is not a json, but a plain text
    logger.info("Letter: %s", letter)

    # Get child's feedback
    logger.info("Getting child's feedback...")
    child_result = make_post_request("/child", json={"story": letter})
    room_code = child_result.json()["room_code"]  # The "feedback" field is only some text, we don't need it
    if not room_code:
        # If we read the right letter and don't get the room code, it means that the key is not valid anymore
        # Since all keys are renewed every 10 seconds, we have to try the whole process again
        raise PermissionError("Unauthorized")
    logger.info("Getting room code: %s", room_code)

    # Get vaults
    logger.info("Getting vaults...")
    room_result = make_get_request("/room", params={"room_code": room_code})
    vaults = room_result.json()
    logger.info("Total vaults: %s", len(vaults))

    # Get vault's content
    for vault in vaults:
        logger.info("Getting %s content...", vault["name"])
        vault_result = make_post_request("/vault", json={"name": vault["name"], "password": vault["password"]})
        content = vault_result.json()["content"]

        if content:
            logger.info("GIFT CARD found in the %s, content: %s", vault["name"], content)
            break  # Gift card found, no need to continue
        else:
            logger.info("Empty content for %s", vault["name"])


if __name__ == "__main__":
    try:
        try:
            main()
        except PermissionError as permission_error:
            # If we get a permissions error (http 401), it means that the key is not valid anymore.
            # Since all keys are renewed every 10 seconds, there was no sufficient time for the 
            # program to execute all the steps. So we just need to try again.
            logger.info("Permission denied, trying again...")
            main()
    except Exception as error:
        logger.error("Something went wrong: %s", error)
