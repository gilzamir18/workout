from uuid import uuid4
from pydantic import UUID4
from fastapi import APIRouter, status, Body
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.contrib.dependencies import DatabaseDependence
from workout_api.categorias.models import CategoriaModel
from sqlalchemy.future import select
from fastapi.exceptions import HTTPException
router = APIRouter()

@router.post(path="/", 
             summary="Criar uma nova categoria", 
             status_code=status.HTTP_201_CREATED, 
             response_model=CategoriaOut)
async def post(dbsession: DatabaseDependence, 
               categoria_in: CategoriaIn = Body(...)) -> CategoriaOut:
    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_in.model_dump())
    dbsession.add(categoria_model)
    await dbsession.commit()
    return categoria_out

@router.get(path="/", 
            summary="retornar todas as categorias", 
            status_code=status.HTTP_200_OK, 
            response_model=list[CategoriaOut])
async def query(dbsession: DatabaseDependence) -> list[CategoriaOut]:
    categorias : list[CategoriaOut] = (await dbsession.execute(select(CategoriaModel))).scalars().all()
    return categorias


@router.get(path="/(id)", 
            summary="retornar uma categoria pelo id", 
            status_code=status.HTTP_200_OK, 
            response_model=CategoriaOut)
async def query(id:UUID4, dbsession: DatabaseDependence) -> CategoriaOut:
    categoria : CategoriaOut = (await dbsession.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()
    if not categoria:
        raise HTTPException(status_code=404, detail=f"Categoria não encontrada no id {id}.")
    return categoria
