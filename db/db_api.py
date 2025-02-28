from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.models import AccountModel, WalletModel

engine = create_engine('sqlite:///db.db')
session = Session(engine)


def update_account_info(
        account_id: int,
        new_authorization_key: str | None = None,
        uid: int | None = None,
        is_registered: bool = False,
        total_points: int | None = None,
        is_twitter_connected: bool = False,
) -> None:
    """
    Функция обновление информации об аккаунте в БД.
    Args:
        account_id:
        new_authorization_key:
        uid:
        is_registered:
        total_points:
        is_twitter_connected:

    Returns:

    """
    try:
        # Находим аккаунт по ID
        account: AccountModel = session.query(AccountModel).filter(AccountModel.id == account_id).one_or_none()

        if account is not None:
            # Обновляем email
            if new_authorization_key:
                account.authorization_key = new_authorization_key
            if uid:
                account.uid = uid
            if is_registered:
                account.is_registered = is_registered
            if total_points:
                account.total_points = total_points
            if is_twitter_connected:
                account.twitter_connection_status = is_twitter_connected
            session.commit()  # Сохраняем изменения в базе данных
        else:
            print(f"Аккаунт с ID {account_id} не найден.")
    except Exception as e:
        session.rollback()  # В случае ошибки откатываем изменения
        print(f"Произошла ошибка: {e}")
    finally:
        session.close()  # Закрываем сеанс


def update_wallet_info(
        wallet_id: int,
        address: str | None = None,
        private_key: str | None = None,
        wallet_connection_status: bool = False
) -> None:
    """
    Функция обновление информации о кошельке в БД.
    Args:
        wallet_id:
        address:
        private_key:
        wallet_connection_status:

    Returns:
        None
    """
    try:
        wallet_account: WalletModel = session.query(WalletModel).filter(WalletModel.id == wallet_id).one_or_none()

        if wallet_account is not None:
            if address:
                wallet_account.address = address
            if private_key:
                wallet_account.private_key = private_key
            if wallet_connection_status:
                wallet_account.wallet_connection_status = wallet_connection_status

            session.commit()
        else:
            logger.info(f"Аккаунт с ID {wallet_account} не найден.")
    except Exception as e:
        session.rollback()  # В случае ошибки откатываем изменения
        logger.error(f"Произошла ошибка: {e}")
    finally:
        session.close()


def load_accounts(is_register: bool = False, is_connect_social: bool = False) -> tuple[list[AccountModel], list[WalletModel]] | None:
    """
    Функция выгрузки аккаунтов из БД.
    Args:
        is_register: Импортировать ли аккаунты для регистрации.
        is_connect_social: Импортировать ли аккаунты для привязки твиттера.

    Returns:
        accounts, account_wallets:
    """
    try:
        if is_register:
            accounts: list[AccountModel] = session.query(AccountModel).filter(AccountModel.is_registered == False).all()
        elif is_connect_social:
            accounts: list[AccountModel] = session.query(AccountModel).filter(AccountModel.twitter_connection_status == False).all()
        elif is_register is False:
            accounts: list[AccountModel] = session.query(AccountModel).filter(AccountModel.is_registered == True).all()

        account_ids = [account.id for account in accounts]
        account_wallets: list[WalletModel] = session.query(WalletModel).filter(WalletModel.id.in_(account_ids)).all()

        if accounts:
            return accounts, account_wallets
        else:
            logger.info("Нет не зарегистрированных аккаунтов.")
            return None
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
    finally:
        session.close()

