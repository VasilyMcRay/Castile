from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
     pass


class AccountModel(Base):
    """
    Базовая модель аккаунта для БД.
    """
    __tablename__ = 'user_account'

    id: Mapped[int] = mapped_column(primary_key=True)
    mail: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    twitter_auth: Mapped[str] = mapped_column()
    proxy: Mapped[str] = mapped_column(default=None, server_default='')
    headers: Mapped[str] = mapped_column(default=None, server_default='')
    cookies: Mapped[str] = mapped_column(default=None, server_default='')
    authorization_key: Mapped[str] = mapped_column(default=None, server_default='')
    uid: Mapped[int] = mapped_column(default=None, server_default='')
    is_registered: Mapped[bool] = mapped_column(default=False, server_default='0')
    total_points: Mapped[int] = mapped_column(default=0, server_default='')
    wallet_id: Mapped[int] = mapped_column(ForeignKey('wallet.id'))
    wallet: Mapped['WalletModel'] = relationship(
        back_populates='account'
    )
    twitter_connection_status: Mapped[bool] = mapped_column(default=False, server_default='0')


class WalletModel(Base):
    """
    Базовая модель кошелька для БД.
    """
    __tablename__ = 'wallet'

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(default=None, server_default='')
    private_key: Mapped[str] = mapped_column(default=None, server_default='')
    wallet_connection_status: Mapped[bool] = mapped_column(default=False, server_default='0')
    account: Mapped['AccountModel'] = relationship(back_populates='wallet', cascade="all, delete-orphan")

