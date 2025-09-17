from flask_sqlalchemy import SQLAlchemy
from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    favorites_list: Mapped[List["Favorites"]] = relationship(
        back_populates="user", cascade="all, delete-orphan")

    # is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites_list": [fav.serialize() for fav in self.favorites_list]
            # do not serialize the password, its a security breach
        }


class Favorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    target_type: Mapped[str] = mapped_column(unique=False, nullable=False)
    target_id: Mapped[int] = mapped_column(unique=False, nullable=False)
    target_name: Mapped[str] = mapped_column(unique=False, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="favorites_list")

    def get_target_favorite(self):
        if self.target_type == "people":
            return db.session.get(People, self.target_id)
        elif self.target_type == "planets":
            return db.session.get(Planets, self.target_id)
        return None

    def serialize(self):
        return {
            "id": self.id,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "target_name": self.target_name,
            "user_id": self.user_id
        }


class People(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=False, nullable=False)
    hair_color: Mapped[str] = mapped_column(unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "hair_color": self.hair_color
        }


class Planets(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=False, nullable=False)
    diameter: Mapped[str] = mapped_column(unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter
        }
