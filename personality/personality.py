import json

from config.config import DEFAULT_PERSONALITIES_FILE_PATH


class Personality:
    def __init__(self, name: str, avatar: str, description: str):
        self.name = name
        self.avatar = avatar
        self.description = description


def load_personalities(filename=DEFAULT_PERSONALITIES_FILE_PATH):
    with open(filename, "r") as file:
        data = json.load(file)
    return [Personality(p["name"], p["avatar"], p["description"]) for p in data["personalities"]]
