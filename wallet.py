import os
import asyncio

from aptos_sdk.account import Account
from aptos_sdk.async_client import RestClient, FaucetClient
from aptos_sdk.asymmetric_crypto import Signature


class Wallet:
    """
    Класс описывающий взаимодействие с кошельком Petra Wallet.
    """
    account: Account
    NODE_URL = os.getenv("APTOS_NODE_URL", "https://api.devnet.aptoslabs.com/v1")
    FAUCET_URL = os.getenv(
        "APTOS_FAUCET_URL",
        "https://faucet.devnet.aptoslabs.com",
    )

    def __init__(self, private_key: str | None = None):
        self.rest_client = RestClient(self.NODE_URL)
        self.faucet_client = FaucetClient(self.FAUCET_URL, self.rest_client)
        if private_key:
            self.account = Account.load_key(private_key)
        else:
            self.account = Account.generate()

    def __str__(self):
        return f'Account address: {self.account.address()}, account private_key: {self.account.private_key}'

    async def sign_message(self, message: str) -> str:
        """
        Функция подписи переданного сообщения.
        :param message:
        :return:
        """
        signature: Signature = self.account.sign(message.encode('utf-8'))
        return str(signature)
