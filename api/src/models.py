import enum

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import ARRAY, ENUM, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# from sqlmodel import ARRAY, JSON, Column, Enum, Field, Integer, SQLModel


class Base(DeclarativeBase):
    """."""

    pass


# Many-to-many relationship between characters and scenes
# (e.g. a character can be in multiple scenes and a scene can have multiple characters)
scenes_characters = Table(
    "scenes_characters",
    Base.metadata,
    Column("scene_id", Integer, ForeignKey("scenes.id", ondelete="CASCADE")),
    Column("character_id", Integer, ForeignKey("characters.id", ondelete="CASCADE")),
)

# Many-to-many relationship between characters and cast members
# (e.g. a character can be played by multiple cast members and a cast member can play
#  multiple characters)
characters_cast_members = Table(
    "characters_cast_members",
    Base.metadata,
    Column("cast_member_id", Integer, ForeignKey("cast_members.id", ondelete="CASCADE")),
    Column("character_id", Integer, ForeignKey("characters.id", ondelete="CASCADE")),
)

# Define the association table for the many-to-many relationship between cast members and rehearsals
cast_members_rehearsals = Table(
    "cast_members_rehearsals",
    Base.metadata,
    Column("cast_member_id", Integer, ForeignKey("cast_members.id")),
    Column("rehearsal_id", Integer, ForeignKey("rehearsals.id")),
)


class User(Base):
    """."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)  # noqa: A003
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    age: Mapped[int | None] = mapped_column(Integer)
    cast_members: Mapped[list["CastMember"]] = relationship("CastMember", back_populates="user")


class CastRole(enum.Enum):
    """."""

    DIRECTOR = enum.auto()
    ACTOR = enum.auto()


class CastMember(Base):
    """."""

    __tablename__ = "cast_members"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)  # noqa: A003
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True, autoincrement=False
    )
    play_id: Mapped[int] = mapped_column(
        ForeignKey("plays.id"), primary_key=True, autoincrement=False
    )
    availability: Mapped[JSON] = mapped_column(JSON, default={})
    roles: Mapped[ARRAY] = mapped_column(ARRAY(ENUM(CastRole)), default=[])
    characters: Mapped[list["Character"]] = relationship(
        "Character",
        secondary=characters_cast_members,
        back_populates="cast_members",
        passive_deletes=True,
    )
    user: Mapped[User] = relationship("User", back_populates="cast_members", passive_deletes=True)
    rehearsals: Mapped[list["Rehearsal"]] = relationship(
        "Rehearsal", secondary=cast_members_rehearsals, back_populates="cast_members"
    )

    # __table_args__ = (PrimaryKeyConstraint("play_id", "user_id"),)


class Play(Base):
    """."""

    __tablename__ = "plays"

    id: Mapped[int | None] = mapped_column(  # noqa: A003
        primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    original_author_name: Mapped[str | None] = mapped_column(String(255))
    genre: Mapped[str | None] = mapped_column(String(255))
    year: Mapped[int | None] = mapped_column(Integer)
    performance_dates: Mapped[list[int] | None] = mapped_column(ARRAY(Integer))
    estimated_duration_sec: Mapped[int | None] = mapped_column(Integer)


class Scene(Base):
    """."""

    __tablename__ = "scenes"

    id: Mapped[int | None] = mapped_column(  # noqa: A003
        primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(255))
    play_id: Mapped[int] = mapped_column(ForeignKey("plays.id"))
    characters: Mapped[list["Character"]] = relationship(
        "Character",
        secondary=scenes_characters,
        back_populates="scenes",
        passive_deletes=True,
    )


class Character(Base):
    """."""

    __tablename__ = "characters"

    id: Mapped[int | None] = mapped_column(  # noqa: A003
        primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(255))
    play_id: Mapped[int] = mapped_column(ForeignKey("plays.id"))

    scenes: Mapped[list["Scene"]] = relationship(
        "Scene",
        secondary=scenes_characters,
        back_populates="characters",
        passive_deletes=True,
    )
    cast_members: Mapped[list["CastMember"]] = relationship(
        "CastMember",
        secondary=characters_cast_members,
        back_populates="characters",
        passive_deletes=True,
    )


class Rehearsal(Base):
    """."""

    __tablename__ = "rehearsals"

    id: Mapped[int] = mapped_column(  # noqa: A003
        primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(255))
    play_id: Mapped[int] = mapped_column(ForeignKey("plays.id"))
    # multiple scenes can be rehearsed at the same time
    scene_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    time_start: Mapped[int] = mapped_column(Integer)
    time_end: Mapped[int] = mapped_column(Integer)
    location: Mapped[str] = mapped_column(String(255))
    cast_member_creator_id: Mapped[int] = mapped_column(ForeignKey("cast_members.id"))
    cast_members: Mapped[list["CastMember"]] = relationship(
        "CastMember", secondary=cast_members_rehearsals, back_populates="rehearsals"
    )
