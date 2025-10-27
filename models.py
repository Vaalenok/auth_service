import datetime
import uuid
import pytz
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    password_hash: Mapped[str] = mapped_column()
    role: Mapped["Roles"] = relationship("Roles", lazy="selectin", back_populates="users")

    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(pytz.timezone("Europe/Moscow")).replace(tzinfo=None)
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(pytz.timezone("Europe/Moscow")).replace(tzinfo=None)
    )
    last_login_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(pytz.timezone("Europe/Moscow")).replace(tzinfo=None)
    )

class Roles(Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column()
    rules: Mapped[list["AccessRule"]] = relationship(
        "AccessRule",
        lazy="selectin",
        back_populates="role",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

class AccessRule(Base):
    __tablename__ = "access_rules"

    production_element: Mapped["ProductionElement"] = relationship("ProductionElement", lazy="selectin", back_populates="access_rules")
    read_permission: Mapped[bool] = mapped_column(default=False)
    create_permission: Mapped[bool] = mapped_column(default=False)
    update_permission: Mapped[bool] = mapped_column(default=False)
    delete_permission: Mapped[bool] = mapped_column(default=False)

    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"))
    element_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("elements.id", ondelete="CASCADE"))

class ProductionElement(Base):
    __tablename__ = "elements"

    name: Mapped[str] = mapped_column()

    access_rules: Mapped[list["AccessRule"]] = relationship(
        "AccessRule",
        lazy="selectin",
        back_populates="production_element",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
