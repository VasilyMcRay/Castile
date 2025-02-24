from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from sqlalchemy.orm import mapped_column, Session


class Base(DeclarativeBase):
     pass


class AccountModel(Base):
    __tablename__ = 'user_account'

    id: Mapped[int] = mapped_column(primary_key=True)
    mail: Mapped[str]
    password: Mapped[str]
    twitter_auth: Mapped[str]
    proxy: Mapped[str] = mapped_column(default=None, server_default='')
    headers: Mapped[str] = mapped_column(default=None, server_default='')
    cookies: Mapped[str] = mapped_column(default=None, server_default='')
    authorization_key: Mapped[str] = mapped_column(default=None, server_default='')
    uid: Mapped[int] = mapped_column(default=None, server_default='')
    wallet_id: Mapped[int] = mapped_column(ForeignKey('wallet.id'))
    wallet: Mapped['WalletModel'] = relationship(
        back_populates='account'
    )


class WalletModel(Base):
    __tablename__ = 'wallet'

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str]
    private_key: Mapped[str]
    # account_id: Mapped[int] = mapped_column(ForeignKey('user_account.id'))
    account: Mapped['AccountModel'] = relationship(back_populates='wallet', cascade="all, delete-orphan")

engine = create_engine('sqlite:///db.db')
Base.metadata.create_all(engine)

# Пример использования сессии
with Session(engine) as session:


    new_account = AccountModel(mail='test1@yandex.ru', password='test', twitter_auth='test_tw_auth')
    new_wallet = WalletModel(address='test_address', private_key='test_private_key')

    new_account.wallet = new_wallet

    session.add(new_account)
    session.commit()