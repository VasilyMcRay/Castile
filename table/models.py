from dataclasses import dataclass


@dataclass
class AccountCSV:
    """
    CSV модель аккаунта.
    """
    header = ['mail', 'password', 'twitter_auth', 'proxy', 'headers', 'cookies', 'authorization_key', 'uid', 'private_key']

    def __init__(
            self, mail: str,
            password: str,
            twitter_auth: str,
            proxy: str = '',
            headers: str = '',
            cookies: str = '',
            authorization_key: str = '',
            uid: str = '',
            private_key: str = ''
    ):
        self.mail = mail
        self.password = password
        self.twitter_auth = twitter_auth
        self.proxy = proxy
        self.headers = headers
        self.cookies = cookies
        self.authorization_key = authorization_key
        self.uid = uid
        self.private_key = private_key

    def __repr__(self):
        return f'{self.mail}'
