from pydantic import BaseModel, Field, PositiveFloat
from typing import Annotated
from workout_api.contrib.schemas import BaseSchema
from pydantic import Field, UUID4

class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description="nome do centro", example="King KD", max_length=20)]
    endereco: Annotated[str, Field(description="endereço", example="Rua da Cola", max_length=60)]
    proprietario: Annotated[str, Field(description="proprietário", example="João Silva", max_length=30)]

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description="nome do centro", example="King KD", max_length=20)]

class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(nome="Identificador")]
    