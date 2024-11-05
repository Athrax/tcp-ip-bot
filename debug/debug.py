from config.config import DEBUG_MODE


def debug(message: str) -> None:
    if DEBUG_MODE:
        print(message)
