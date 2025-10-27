import uuid
from sqlalchemy import select
from typing import Type
from database import connection, Base

@connection(commit=False)
async def get(model: Type[Base], _id: uuid.UUID, session):
    result = await session.execute(select(model).filter_by(id=_id))
    _object = result.scalars().first()
    return _object

@connection(commit=False)
async def get_all(model: Type[Base], session):
    result = await session.execute(select(model))
    objects = result.scalars().all()
    return objects

@connection()
async def create(new_object: Base, session):
    session.add(new_object)
    await session.flush()
    return new_object

@connection()
async def update(updated_object: Base, session):
    await session.merge(updated_object)
    await session.flush()

@connection()
async def delete(model: Type[Base], _id: uuid.UUID, session):
    _object = await get(model, _id)
    await session.delete(_object)
