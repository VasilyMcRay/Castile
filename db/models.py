from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from sqlalchemy.orm import mapped_column


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
    address: Mapped[str] = mapped_column(default=None, server_default='')
    private_key: Mapped[str] = mapped_column(default=None, server_default='')
    account: Mapped['AccountModel'] = relationship(back_populates='wallet', cascade="all, delete-orphan")