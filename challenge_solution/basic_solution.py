import requests

BASE_URL = "https://challenge.ivanbicalho.com"


# Getting the key
print("Getting key...")
result = requests.get(BASE_URL + "/key")
if result.status_code != 200:
    print("Something went wrong: %s", result.content)
key = result.json()["key"]
print("Key:", key)


# Opening the box
print("Opening the box...")
result = requests.get(BASE_URL + "/box", params={"box_key": key})
if result.status_code != 200:
    print("Something went wrong:", result.content)
    exit()
letter = result.text  # The response here is not a json, but a plain text
print("Letter:", letter)


# Get child's feedback
print("Getting child's feedback...")
result = requests.post(BASE_URL + "/child", json={"story": letter})
if result.status_code != 200:
    print("Something went wrong:", result.content)
    exit()
room_code = result.json()["room_code"]  # The "feedback" field is only some text, we don't need it
print("Room code:", room_code)


# Getting vaults
print(f"Getting vaults...")
result = requests.get(BASE_URL + "/room", params={"room_code": room_code})
if result.status_code != 200:
    print("Something went wrong:", result.content)
    exit()
vaults = result.json()
print(f"Total vaults:", len(vaults))


for vault in vaults:
    # Get vault's content
    print(f"Getting {vault['name']} content...")
    result = requests.post(BASE_URL + "/vault", json={"name": vault["name"], "password": vault["password"]})
    if result.status_code != 200:
        print("Something went wrong:", result.content)
        exit()
    content = result.json()["content"]

    if content:
        print(f"GIFT CARD found in the {vault['name']}:", content)
        break  # Gift card found, no need to continue
    else:
        print(f"Empty content for {vault['name']}")
