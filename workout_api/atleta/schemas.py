from pydantic import BaseModel, Field, PositiveFloat
from typing import Annotated, Optional
from workout_api.contrib.schemas import BaseSchema, OutMixin
from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description="nome do atleta", example="Joao", max_length=50)]
    cpf: Annotated[str, Field(description="cpf do atleta", example="12345678900", max_length=11)]
    idade: Annotated[int, Field(description="idade do atleta", example=25)]
    peso: Annotated[PositiveFloat, Field(description="peso do atleta", example=70)]
    altura: Annotated[PositiveFloat, Field(description="altura do atleta", example=1.70)]
    sexo: Annotated[str, Field(description="sexo do atleta", example="M", max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description="categoria do atleta", )]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="centro de treinamento do atleta", )]

class AtletaIn(Atleta):
    pass

class AtletaOut(Atleta, OutMixin):
    pass

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description="nome do atleta", example="Joao", max_length=50)]
    idade: Annotated[Optional[int], Field(None, description="idade do atleta", example=25)]

class AtletaResumido(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description="nome do atleta", example="Joao", max_length=50)]
    categoria: Annotated[CategoriaIn, Field(description="categoria do atleta", )]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="centro de treinamento do atleta", )]
