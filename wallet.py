import os
import asyncio

from aptos_sdk.account import Account
from aptos_sdk.async_client import RestClient, FaucetClient
from aptos_sdk.asymmetric_crypto import Signature
from aptos_sdk.bcs import Serializer
from aptos_sdk.transactions import EntryFunction, TransactionPayload, TransactionArgument
from aptos_sdk.type_tag import TypeTag, StructTag
from loguru import logger


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
        # self.faucet_client = FaucetClient(self.FAUCET_URL, self.rest_client)
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
        """
        signature: Signature = self.account.sign(message.encode('utf-8'))
        return str(signature)

    async def make_daily_transaction(self) -> str:
        """
        Функция подписания ежедневной транзакции.
        """
        logger.info(self.account.address())
        transaction_argument = TransactionArgument(self.account.address(), Serializer.struct)
        payload = EntryFunction.natural(
            '0x3fa9e346261bdd3bdd7bbc57b1cb12b47a5ae8cb7531b6fa4759f524ffcac011::my_counter',
            'increment',
            [],
            [
                transaction_argument
            ],
        )
        signed_transaction = await self.rest_client.create_bcs_signed_transaction(
            self.account, payload=TransactionPayload(payload)
        )
        logger.info(f'signed_transaction: {signed_transaction}')
        tx = await self.rest_client.submit_bcs_transaction(signed_transaction)
        logger.info(f'tx: {tx}')
        return tx