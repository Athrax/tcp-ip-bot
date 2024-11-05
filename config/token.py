from config.messages import TOKEN_FILE_NOT_FOUND


def token_loader(file_path: str) -> str:
    try:
        with open(file_path, "r") as f:
            token: str = f.read()
        return token
    except FileNotFoundError:
        raise Exception(TOKEN_FILE_NOT_FOUND)