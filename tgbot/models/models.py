from gino import Gino
from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, ForeignKey, Date

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
    balance = Column(
        Integer,
        nullable=False,
        default=0
    )
    subscribed_date = Column(Date)

    def __str__(self):
        return f"{self.phone_number}"

    def __repr__(self):
        return f"{self.phone_number}"


class Draw(db.Model):

    __tablename__ = "draw"

    Id = Column(Integer, primary_key=True)
    name = Column(String(100))
    title = Column(String(200))
    preview_photo_path = Column(String)
    active = Column(Boolean, default=True)
    cancelled = Column(Boolean, default=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    winners_count = Column(Integer)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class DrawMember(db.Model):

    __tablename__ = "draw_member"

    Id = Column(Integer, primary_key=True)
    member = Column(Integer, ForeignKey("subscriber.Id"))
    draw = Column(Integer, ForeignKey("draw.Id"))
    winner = Column(Boolean, default=False)

    def __str__(self):
        return f"{self.member}: {self.draw}"

    def __repr__(self):
        return f"{self.member}: {self.draw}"
