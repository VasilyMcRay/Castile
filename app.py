import asyncio

from loguru import logger

from account import  Account
from Import import Import
from db.db_api import load_accounts, update_wallet_info
from data.data import get_headers

def initialize_accounts(is_register: bool = False, is_social_connection: bool = False) -> list[Account]:
    """
    Функция инициализации всех аккаунтов по заданным ключам.
    Args:
        is_register:
        is_social_connection:

    Returns:

    """
    accounts = []
    model_accounts, model_wallets = load_accounts(is_register=is_register, is_connect_social=is_social_connection)
    for model_account, model_wallet in zip(model_accounts, model_wallets):
        if not model_account.headers:
            headers = get_headers()
        else:
            headers = ''
        account = Account(
            id=model_account.id,
            mail=model_account.mail,
            password=model_account.password,
            twitter_auth=model_account.twitter_auth,
            proxy=model_account.proxy,
            headers=headers,
            cookies=None,
            authorization_key=model_account.authorization_key,
            uid=model_account.uid,
            private_key=model_wallet.private_key,
            is_registered=model_account.is_registered
        )
        accounts.append(account)
    return accounts


async def make_base_action(action: int):
    tasks = []
    is_register = False
    is_social_connection = False
    if action == 2:
        is_register = True
    elif action == 4:
        is_social_connection = True
    game_accounts = initialize_accounts(is_register=is_register, is_social_connection=is_social_connection)

    if action == 2 or action == 3:
        for account in game_accounts:
            if not account.is_registered:
                update_wallet_info(
                    wallet_id=account.wallet.id,
                    address=str(account.wallet.account.address()),
                    private_key=str(account.wallet.account.private_key)
                )
            tasks.append(asyncio.create_task(
                account.login_account()
            ))

    elif action == 4:
        for account in game_accounts:
            tasks.append(account.check_complete_base_actions())

    elif action == 5:
        for account in game_accounts:
            tasks.append(account.complete_all_tasks())

    elif action == 6:
        for account in game_accounts:
            tasks.append(account.get_points_info())

    for completed_task in asyncio.as_completed(tasks):
        try:
            await completed_task
        except ValueError:
            logger.error(f'Caught ValueError in task: {completed_task}')





async def main():
    while True:
        print('''  Select the action:
        1) Import accounts from the spreadsheet to the DB;
        2) Start the registration;
        3) Start the login;
        4) Connect wallet and twitter;
        5) Complete all quests
        6) Check total points
        7) Make daily transaction
        8) Exit.''')
        try:
            action = int(input('Выберите действие: '))
            if action == 1:
                Import.db_objects()

            elif action == 2:
                await make_base_action(action)

            elif action == 3:
                await make_base_action(action)

            elif action == 4:
                await make_base_action(action)

            elif action == 5:
                await make_base_action(action)

            elif action == 6:
                await make_base_action(action)

            elif action == 7:
                pass

            elif action == 8:
                logger.info('Программа завершена')
                break


        except KeyboardInterrupt:
            print()

        except ValueError as err:
            logger.error(f'Value error: {err}')

        except BaseException as e:
            logger.error(f'Something went wrong: {e}')

if __name__ == '__main__':
    asyncio.run(main())