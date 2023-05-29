import datetime
import hashlib
import os
from typing import List

from schemas import Vault, VaultContent


def get_pass(input: str) -> str:
    now = datetime.datetime.now()
    input = input + now.strftime("%Y%m%d%H%M") + str(int(now.strftime("%S")) // 10)
    return hashlib.sha256(input.encode()).hexdigest()[0:16]


def get_story() -> str:
    return (
        "Once upon a time, in a magical kingdom nestled among misty mountains and lush green valleys, "
        "a king told to his people: My dear beloved people, in possession of this code you will find "
        f"beauties never seen before in all the history: {get_pass('history')}"
    )


def get_vault_names() -> List[str]:
    return [f"vault{i}" for i in range(1, 11)]


def get_vault(name: str) -> Vault:
    return Vault(name=name, password=get_pass(name))


def get_vault_content(name: str) -> VaultContent:
    vault = get_vault(name)
    content = os.getenv("GIFT_CARD") if name == os.getenv("AWARD_VAULT") else ""
    return VaultContent(name=vault.name, password=vault.password, content=content)
