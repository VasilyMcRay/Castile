import base64
import json
import time

import twitter
from loguru import logger

from base import Base
from wallet import Wallet
from methods import Methods


class Account(Base):
    """
    Класс Castile аккуанта.
    """
    wallet: Wallet
    tw_account: twitter.Account
    def __init__(
            self,
            mail: str,
            password: str,
            twitter_auth: str,
            proxy: str | None,
            headers: dict | None,
            cookies: dict | None = None,
            authorization_key: str | None = None,
            uid: str | None = None,
            private_key: str | None = None
    ):
        super().__init__(proxy=proxy, headers=headers, cookies=cookies)
        self.mail = mail
        self.password = password
        self.wallet = Wallet(private_key=private_key)
        self.uid = uid
        if authorization_key:
            self.headers['authorization'] = f'Bearer {authorization_key}'
        self.authorization_key = authorization_key
        self.tw_account = twitter.Account(auth_token=twitter_auth)

    def __str__(self):
        return f"""
mail: {self.mail}\npassword: {self.password}\ntwitter_auth: {self.tw_account.auth_token}
proxy: {self.proxy}\nheaders: {self.headers}\ncookies: {self.cookies}
authorization: {self.authorization_key}
uid: {self.uid}\nprivate_key: {self.wallet.account.private_key}
"""

    def write_data(self, data: dict) -> None:
        """
        Функция записи данных от аккаунта.
        :param data:
        :return:
        """
        self.uid = data['uid']
        self.authorization_key = data['auth']
        self.headers['authorization'] = f'Bearer {self.authorization_key}'
        data['password'] = self.password
        data['wallet_address'] = str(self.wallet.account.address())
        data['private_key'] = str(self.wallet.account.private_key)
        with open('data/outputs.json', 'w') as file:
            json.dump(data, file)
            file.write('\n')

    async def get_user_info(self) -> dict:
        url = 'https://castile.world/api/user/pullUserInfo'
        user_info = await self.get_base_session(Methods.POST, url=url)
        logger.info(f'user info: {user_info}')
        return user_info

    async def register_account(self) -> dict:
        """
        Фугкция регистрации аккаунта на Castile
        :return:
        """
        url = 'https://castile.world/api/guest/register'
        json_data = {
            'email': self.mail,
            'code': '888888',
            'password': self.password,
            'password_confirm': self.password,
            'agree': True,
        }

        data = await self.get_base_session(Methods.POST, url=url, json=json_data)
        logger.info('Успешно зарегестрировал аккаунт')
        self.write_data(data['data'])
        return data

    async def login_account(self) -> dict:
        url = 'https://castile.world/api/guest/login'
        json_data = {
            'email': self.mail,
            'password': self.password,
        }
        try:
            data = await self.get_base_session(Methods.POST, url=url, json=json_data)
            logger.info(f'Got data after login: {data}')
            if data.get('status', {}).get('msg') == 'User does not exist':
                data = await self.register_account()
            self.write_data(data['data'])
            return data
        except Exception as error:
            logger.error(error)
            return {}

    async def get_points_info(self):
        url = 'https://castile.world/api/task/pointsInfo'
        json_data = {}
        data = await self.get_base_session(Methods.POST, url=url, json=json_data)
        points_info = data.get('data')
        logger.info(f'Points info {points_info}')
        return data

    async def get_bind_status(self) -> dict:
        """
        Функция проверки подключения кошелька к аккаунту.
        :return:
        """
        #todo: Проверить код возврата 10404 и 10200
        url = 'https://castile.world/api/user/getBindStatus'
        json_data = {
            'address': str(self.wallet.account.address()),
        }
        data = await self.get_base_session(Methods.POST, url=url, json=json_data)
        wallet_status_code = data.get('status', {}).get('code')
        logger.info(f'Успешно получил статус привязки кошелька {wallet_status_code}')
        return wallet_status_code

    async def bind_wallet(self) -> dict:
        bind_status = await self.get_bind_status()
        if bind_status == 10200:
            logger.info(f'Wallet {self.wallet.account.address()} already connected to {self.mail} account')
            return bind_status

        url = 'https://castile.world/api/user/bindWallet'
        current_time = int(time.time())
        rounded_time = int(current_time - current_time % 3600)
        message = f'Welcome to the Castile platform’s wallet management process. By clicking to sign in, you are initiating the linking of your wallet address to your Castile account as a deposit wallet. This request will not trigger a blockchain transaction or cost any gas fees.'
        full_message = f'APTOS\nmessage: {message}\nnonce: {rounded_time}'
        sign = await self.wallet.sign_message(full_message)
        byte_array = bytes.fromhex(sign[2:])
        # Кодируем в Base64
        base64_sign = base64.b64encode(byte_array).decode('utf-8')
        json_data = {
            'sign': base64_sign,
            'publicKey': str(self.wallet.account.public_key()),
            'address': str(self.wallet.account.address()),
            'wallet': 'Petra',
            'message': full_message,
            'type': 'Aptos',
        }
        bind_status = await self.get_base_session(Methods.POST, url=url, json=json_data)
        wallet_status_code = bind_status.get('status', {}).get('code')
        if wallet_status_code == 10200:
            logger.info(f'Wallet {self.wallet.account.address()}was connected to {self.mail} account')
        return bind_status

    async def authorize_twitter(self):

        original_string = f'{self.uid}|bind_twitter|'
        bytes_string = original_string.encode('utf-8')
        base64_encoded = base64.b64encode(bytes_string)
        state = base64_encoded.decode('utf-8')
        oauth2_data = {
                'response_type': 'code',                                             # static
                'client_id': 'VktCa2VJcjVsdkZoSnFDLUpHanQ6MTpjaQ',                   # static
                'redirect_uri': 'https://www.castile.world/api/twitter/receive',     # static
                'scope': 'users.read tweet.read',                                    # static
                'state': state,                                                      # not static MzczODk3fGJpbmRfdHdpdHRlcnw=
                'code_challenge': 'challenge',                                       # static
                'code_challenge_method': 'plain'                                     # static
            }
        async with twitter.Client(
                self.tw_account,
                proxy=self.proxy,
        ) as twitter_client:
            auth_code = await twitter_client.oauth2(**oauth2_data)

        logger.info(f'auth code: {auth_code}')
        return state, auth_code

    async def verify_castile_twitter(self):
        url = 'https://www.castile.world/api/twitter/receive'
        state, auth_code = await self.authorize_twitter()
        params = {
            'state': state,
            'code': auth_code,
        }
        result = await self.get_base_session(Methods.GET, url=url, params=params, is_verify_twitter=True)
        logger.info(f'Успешно привязал твиттер {self.tw_account.auth_token} к аккаунту {self.mail}')
        return result

    async def check_complete_base_actions(self):
        """
        Функция выполнения 1) Регистрации/Логина 2) Привязки кошелька 3) Привязки Твиттера
        :return:
        """
        user_info = await self.get_user_info()
        if user_info.get('status', {}).get('code') == 403:
            logger.info('User not logged in')
            await self.login_account()
            user_info = await self.get_user_info()
        await self.bind_wallet()
        if user_info.get('data', {}).get('twitter_id') == 0:
            logger.info('twitter not connected')
            await self.verify_castile_twitter()