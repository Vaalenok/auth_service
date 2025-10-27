import datetime
import uuid
import pytz
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database import Base

def now_naive():
    return datetime.datetime.now(pytz.timezone("Europe/Moscow")).replace(tzinfo=None)

class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    password_hash: Mapped[str] = mapped_column()
    role: Mapped["Roles"] = relationship(
        "Roles",
        back_populates="users",
        lazy="selectin"
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=now_naive())
    updated_at: Mapped[datetime.datetime] = mapped_column(default=now_naive())
    last_login_at: Mapped[datetime.datetime] = mapped_column(default=now_naive())

    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("roles.id", ondelete="SET NULL"),
        nullable=True
    )

class Roles(Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column()

    users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="role",
        cascade="save-update",
        passive_deletes=True
    )
    rules: Mapped[list["AccessRule"]] = relationship(
        "AccessRule",
        back_populates="role",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

class AccessRule(Base):
    __tablename__ = "access_rules"

    read_permission: Mapped[bool] = mapped_column(default=False)
    create_permission: Mapped[bool] = mapped_column(default=False)
    update_permission: Mapped[bool] = mapped_column(default=False)
    delete_permission: Mapped[bool] = mapped_column(default=False)

    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False
    )
    element_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("production_elements.id", ondelete="CASCADE"),
        nullable=False
    )
    role: Mapped["Roles"] = relationship(
        "Roles",
        back_populates="rules",
        lazy="selectin"
    )
    production_element: Mapped["ProductionElement"] = relationship(
        "ProductionElement",
        back_populates="access_rules",
        lazy="selectin"
    )

class ProductionElement(Base):
    __tablename__ = "production_elements"

    name: Mapped[str] = mapped_column()

    access_rules: Mapped[list["AccessRule"]] = relationship(
        "AccessRule",
        back_populates="production_element",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
