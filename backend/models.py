from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

# ✔ Base declarativa correta para SQLAlchemy 2.x
Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(500), nullable=False)

    carts = relationship(
        "Cart",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(String(20), default="open", nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )

    user = relationship("User", back_populates="carts")

    items = relationship(
        "Item",
        back_populates="cart",
        cascade="all, delete-orphan"
    )


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    frequency = Column(Integer, default=0, nullable=False)

    cart_id = Column(
        Integer,
        ForeignKey("cart.id", ondelete="CASCADE"),
        nullable=False
    )

    cart = relationship("Cart", back_populates="items")
