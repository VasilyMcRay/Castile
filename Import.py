import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from table.models import AccountCSV, WalletCsv
from db.models import AccountModel, WalletModel, Base


class CSV:
    """
    Класс для работы с CSV файлами.
    """
    @staticmethod
    def get_accounts_from_csv(path: str = 'data/input.csv', is_first_iter: bool = True) -> list[AccountCSV]:
        """
        Функция для получения объектов класса AccounCSV из csv файла.
        Args:
            path: Путь
            is_first_iter: Флаг первой итерации

        Returns:
            list[AccountCSV]
        """
        accounts = []
        with open(path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if is_first_iter:
                    is_first_iter = False
                    continue
                row = row[0].split(';')
                accounts.append(
                    AccountCSV(
                        mail=row[0],
                        password=row[1],
                        twitter_auth=row[2],
                        proxy=row[3],
                        headers=row[4],
                        cookies=row[5],
                        authorization_key=row[6],
                        uid=row[7],
                        private_key=row[8],
                    )
                )
        return accounts

class Import:
    """
    Класс импорта и создания объектов в БД
    """
    @staticmethod
    def create_db_object() -> list[AccountModel]:
        """
        Создание объектов класса AccountModel
        Returns:

        """
        db_objects = []
        csv_accounts = CSV.get_accounts_from_csv()
        for account in csv_accounts:
            db_wallet = WalletModel(
                private_key=account.private_key
            )
            db_account = AccountModel(
                mail=account.mail,
                password=account.password,
                twitter_auth=account.twitter_auth,
                proxy=account.proxy,
                headers=account.headers,
                cookies=account.cookies,
                authorization_key=account.authorization_key,
                uid=account.uid,
                wallet=db_wallet,
            )
            db_objects.append(db_account)
        return db_objects

# todo: Вынести в отдельную функцию
objects_for_db = Import.create_db_object()
engine = create_engine('sqlite:///db.db')
Base.metadata.create_all(engine)
with Session(engine) as session:


    new_account = AccountModel(mail='test21@yandex.ru', password='test', twitter_auth='test_tw_auth')
    new_wallet = WalletModel(address='test3_address')

    new_account.wallet = new_wallet

    session.add(new_account)
    session.commit()
