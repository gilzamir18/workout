from typing import Annotated
from workout_api.contrib.schemas import BaseSchema
from pydantic import Field, UUID4

class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(nome="nome da categoria", example="MaxFit", max_length=10)]

class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(nome="Identificador")]