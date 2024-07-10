from fastapi_pagination import Page, Params, paginate
from fastapi import APIRouter, status, Body, Query, Depends
from workout_api.atleta.schemas import AtletaOut, AtletaIn, AtletaUpdate, AtletaResumido
from workout_api.contrib.dependencies import DatabaseDependence
from pydantic import UUID4
from uuid import uuid4
from workout_api.atleta.models import AtletaModel
from sqlalchemy.future import select
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from fastapi.exceptions import HTTPException
from datetime import datetime
from typing import Optional
import sqlalchemy

router = APIRouter()

@router.post(path="/", 
             summary="Criar novo atleta", 
             status_code=status.HTTP_201_CREATED)
async def post(dbsession: DatabaseDependence, 
               atleta_in: AtletaIn = Body(...)
               ):
    
    categoria = (await dbsession.execute(select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome))).scalars().first()
    if not categoria:
        raise HTTPException(
            status_code=400,
            detail=f"A categoria {atleta_in.categoria.nome} não foi encontrada."
        )

    centro = (await dbsession.execute(select(CentroTreinamentoModel).filter_by(nome=atleta_in.centro_treinamento.nome))).scalars().first()
    if not centro:
        raise HTTPException(
            status_code=400,
            detail=f"O centro de treinamento {atleta_in.centro_treinamento.nome} não foi encontrado."
        )

    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro.pk_id

        dbsession.add(atleta_model)
        await dbsession.commit()
    except sqlalchemy.exc.IntegrityError as integrityerror:
        raise HTTPException(
            status_code=409,
            detail=f"Já existe um usuário cadastrado com o cpf {atleta_in.cpf}!"
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocorreu um erro ao inserir os dados no banco!"
        )

    return atleta_out

@router.get(path="/", 
            summary="retornar todos os atletas", 
            status_code=status.HTTP_200_OK, 
            response_model=Page[AtletaOut])
async def query(dbsession: DatabaseDependence, 
                nome: Optional[str] = Query(None), 
                cpf: Optional[str] = Query(None),
                params: Params = Depends()) -> Page[AtletaOut]:       
    async with dbsession as session:
        query = select(AtletaModel)
        
        # Filtrando por nome e cpf, se fornecidos
        if nome:
            query = query.where(AtletaModel.nome == nome)
        if cpf:
            query = query.where(AtletaModel.cpf == cpf)
        
        result = await session.execute(query)
        atletas = result.scalars().all()
    
    return paginate([AtletaOut.model_validate(atleta) for atleta in atletas], params)

@router.get(path="/resumido", 
            summary="retornar todos os atletas com dados resumidos", 
            status_code=status.HTTP_200_OK, 
            response_model=list[AtletaResumido])
async def query(dbsession: DatabaseDependence, nome: Optional[str] = Query(None), cpf: Optional[str] = Query(None)) -> list[AtletaOut]:
    atletas = None
    atletas : list[AtletaResumido] = (await dbsession.execute(select(AtletaModel))).scalars().all()
    return [AtletaResumido.model_validate(atleta) for atleta in atletas] 


@router.get(path="/(id)", 
            summary="retornar um atleta pelo id", 
            status_code=status.HTTP_200_OK, 
            response_model=AtletaOut)
async def query(id:UUID4, dbsession: DatabaseDependence) -> AtletaOut:
    atleta : AtletaOut = (await dbsession.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=404, detail=f"Atleta não encontrado no id {id}.")
    return atleta

@router.patch(path="/(id)", 
            summary="editar um atleta pelo id", 
            status_code=status.HTTP_200_OK, 
            response_model=AtletaOut)
async def query(id:UUID4, dbsession: DatabaseDependence, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta : AtletaOut = (await dbsession.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=404, detail=f"Atleta não encontrado no id {id}.")
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_up:
        setattr(atleta, key, value)

    await dbsession.commit()
    await dbsession.refresh(atleta)
    return atleta

@router.delete(path="/(id)", 
            summary="deleta um atleta pelo id", 
            status_code=status.HTTP_204_NO_CONTENT)
async def query(id:UUID4, dbsession: DatabaseDependence) -> None:
    atleta : AtletaOut = (await dbsession.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=404, detail=f"Atleta não encontrado no id {id}.")
    await dbsession.delete(atleta)
    await dbsession.commit()
