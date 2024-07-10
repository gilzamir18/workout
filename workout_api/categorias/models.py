from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from workout_api.contrib.models import BaseModel
from sqlalchemy.types import Integer, String, Float, DateTime
from datetime import datetime


class CategoriaModel(BaseModel):
    __tablename__ = "categorias"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(10), nullable=False)
    atleta: Mapped['AtletaModel'] = relationship(back_populates='categoria')