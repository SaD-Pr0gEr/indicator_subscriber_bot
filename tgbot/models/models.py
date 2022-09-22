from gino import Gino
from sqlalchemy import Column, Integer, BigInteger, String

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
    is_admin = Column(Boolean)

    def __str__(self):
        return f"{self.username or self.tg_id}"

    def __repr__(self):
        return f"{self.username or self.tg_id}"
