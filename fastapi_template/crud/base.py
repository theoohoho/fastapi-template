from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy import delete, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select
from sqlalchemy.orm import Session


from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def _sql_stmt(
        self,
        select_clauses: Optional[List] = None,
        where_clauses: List = [],
        group_by_clauses: List = [],
        order_by_clauses: List = [],
        join_clauses: List = [],
    ):
        if not select_clauses:
            select_clauses = [self.model]
        sql_stmt = (
            select(*select_clauses)
            .where(*where_clauses)
            .group_by(*group_by_clauses)
            .order_by(*order_by_clauses)
        )
        if join_clauses:
            sql_stmt = sql_stmt.join(*join_clauses)
        return sql_stmt

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        stmt = self._sql_stmt(
            select_clauses=[self.model], where_clauses=[self.model.id == id]
        )
        return db.execute(stmt).scalar_one_or_none()

    def get_multi(self, db: Session, *args, **kwargs) -> List[ModelType]:
        stmt = self._sql_stmt(*args, **kwargs)
        return db.execute(stmt)

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
