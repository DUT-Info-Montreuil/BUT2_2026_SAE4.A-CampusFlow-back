import secrets


class Token:
    token_list: list() = list()

    def __init__(self):
        self.token = secrets.token_hex(16)
        Token.token_list.append(self.token)

    @staticmethod
    def token_ok(token: str):
        if token in Token.token_list:
            return True
        return False

    def get_token(self):
        return self.token
