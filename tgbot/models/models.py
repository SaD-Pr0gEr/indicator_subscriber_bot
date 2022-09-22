from gino import Gino
from sqlalchemy import Column, Integer, BigInteger, String, Boolean

db = Gino()


class Users(db.Model):

    __tablename__ = "subscriber"

    Id = Column(Integer, primary_key=True)
    tg_id = Column(
        BigInteger,
        unique=True,
        nullable=False
    )
    username = Column(String)
    is_admin = Column(
        Boolean,
        nullable=False,
        default=False
    )
    phone_number = Column(
        BigInteger,
        nullable=False,
        unique=True
    )

    def __str__(self):
        return f"{self.phone_number}"

    def __repr__(self):
        return f"{self.phone_number}"
