from uuid import uuid4
from pydantic import UUID4
from fastapi import APIRouter, status, Body
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.contrib.dependencies import DatabaseDependence
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from sqlalchemy.future import select
from fastapi.exceptions import HTTPException
router = APIRouter()

@router.post(path="/", 
             summary="Criar um novo centro de treinamento", 
             status_code=status.HTTP_201_CREATED, 
             response_model=CentroTreinamentoOut)
async def post(dbsession: DatabaseDependence, 
               centro_in: CentroTreinamentoIn = Body(...)) -> CentroTreinamentoOut:
    centro_out = CentroTreinamentoOut(id=uuid4(), **centro_in.model_dump())
    centro_model = CentroTreinamentoModel(**centro_in.model_dump())
    dbsession.add(centro_model)
    await dbsession.commit()
    return centro_out

@router.get(path="/", 
            summary="retornar todos os centros de treinamento", 
            status_code=status.HTTP_200_OK, 
            response_model=list[CentroTreinamentoOut])
async def query(dbsession: DatabaseDependence) -> list[CentroTreinamentoOut]:
    centros : list[CentroTreinamentoOut] = (await dbsession.execute(
                                                select(CentroTreinamentoModel)
                                            )
                                            ).scalars().all()
    return centros

@router.get(path="/(id)", 
            summary="retornar um centro de treinamento pelo id", 
            status_code=status.HTTP_200_OK, 
            response_model=CentroTreinamentoOut)
async def query(id:UUID4, dbsession: DatabaseDependence) -> CentroTreinamentoOut:
    centro : CentroTreinamentoOut = (await dbsession.execute(
                                                                select(CentroTreinamentoModel).
                                                                    filter_by(id=id))
                                    ).scalars().first()
    if not centro:
        raise HTTPException(status_code=404, detail=f"Centro de treinamento não encontrada no id {id}.")
    return centro
