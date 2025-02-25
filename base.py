from curl_cffi.requests import AsyncSession

from utils import format_proxy
from methods import Methods

class Base:
    """
    Базовый класс для создания сессий.
    """
    proxy: str
    headers: dict | None
    cookies: dict | None
    def __init__(self, proxy: str | None, headers: dict | None = None, cookies: dict | None = None):
        if proxy:
            self.proxy = format_proxy(proxy)
        else:
            self.proxy = proxy

        self.headers = headers
        self.cookies = cookies

    async def get_base_session(self, method: str, url: str, is_verify_twitter: bool = False, **kwargs,) -> dict:
        """
        Функция инициализации базововой сессии.
        :return:
        """
        params = kwargs.pop('params', None)
        json_data = kwargs.pop('json', None)

        if method.upper() == Methods.GET:
            async with AsyncSession(proxy=self.proxy, headers=self.headers, cookies=self.cookies) as session:
                response = await session.get(url=url, params=params)
                if is_verify_twitter:
                    return response
                return response.json()

        elif method.upper() == Methods.POST:
            async with AsyncSession(proxy=self.proxy, headers=self.headers, cookies=self.cookies) as session:
                response = await session.post(url=url, json=json_data)
                return response.json()
