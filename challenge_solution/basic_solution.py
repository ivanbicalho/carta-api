import requests

BASE_URL = "http://localhost:8000/challenge"


result = requests.get(BASE_URL + "/key")
# Getting the key
if result.status_code != 200:
    print("Something went wrong: %s", result.content)
key = result.json()["key"]
print("Getting the key: ", key)


# Get the letter
result = requests.get(BASE_URL + "/box", params={"box_key": key})
if result.status_code != 200:
    print("Something went wrong: %s", result.content)
    exit()
letter = result.text  # the response is not a json, but a plain text
print("Getting the letter: ", letter)


# Get the child's feedback
result = requests.post(BASE_URL + "/child", json={"story": letter})
if result.status_code != 200:
    print("Something went wrong: %s", result.content)
    exit()
room_code = result.json()["room_code"]  # The "feedback" field is only some text, we don't need it
print("Getting room code: ", room_code)


# Get the vaults
result = requests.get(BASE_URL + "/room", params={"room_code": room_code})
if result.status_code != 200:
    print("Something went wrong: %s", result.content)
    exit()
vaults = result.json()
print(f"Getting vaults: {len(vaults)} vaults")


for vault in vaults:
    # Get vault's content
    result = requests.post(BASE_URL + "/vault", json={"name": vault["name"], "password": vault["password"]})
    if result.status_code != 200:
        print("Something went wrong: %s", result.content)
        exit()
    content = result.json()["content"]  # The "name" and "password" fields are only some text, we don't need them

    if content:
        print(f"GIFT CARD found in the {vault['name']}:", content)
        break
