import asyncio

from account import Account

from data.data import HEADERS, COOKIES


async def main():
    # account = Account(
    #     mail='vasyqq12@yandex.ru',
    #     password='A12fsaiki43fj',
    #     proxy='user196901:pzik08@80.91.209.248:5546',
    #     headers=HEADERS,
    #     twitter_auth='1a22988a6396f1bb1e069791ccea972b50d037de',
    #     authorization_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIiLCJhdWQiOiIiLCJpYXQiOjE3NDAxNDA0MTYsIm5iZiI6MTc0MDE0MDQxNiwiZXhwIjoxNzQwMjI2ODE2LCJkYXRhIjp7ImlkIjoiMzc0MTY0In19.6EjjsRz4L49yQJyvK_Cf9h5BQ5ibIFBJPIJU1pTdjvw',
    #     private_key='0x76d626b7b7eeedacbce63dc43844e714a5d7cfd68e6f9ecd60415bfb242afe12',
    #     uid='374164'
    # )
    account = Account(
        mail='gl12312@yandex.ru',
        password='A12fsaiki43fj',
        proxy='user196901:pzik08@80.91.209.248:5546',
        headers=HEADERS,
        twitter_auth='9db396881eb200fb18357fe4862c194cae402b94',
        private_key='0xaa536b716fda724eec8f32bbdb519c48c12b0a6e833881b77969c8dde58c270c'
    )
    await account.check_complete_base_actions()
    # await account.get_points_info()
    # print(account)
    # await account.get_user_info()
    # register_result = await account.register_account()
    # print(register_result)
    # await asyncio.sleep(1)
    # print(await account.bind_wallet())
    # await asyncio.sleep(5)
    # print(await account.verify_castile_twitter())
    # await asyncio.sleep(2)
    # await account.get_user_info()

if __name__ == '__main__':
    asyncio.run(main())
