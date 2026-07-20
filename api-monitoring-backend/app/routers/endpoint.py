from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.endpoint import EndpointCreate, EndpointUpdate, EndpointOut
from app.crud import endpoint as crud_endpoint

router = APIRouter(
    prefix="/endpoints",
    tags=["Endpoints"]
)


@router.post("/", response_model=EndpointOut, status_code=status.HTTP_201_CREATED)
def create_endpoint(data: EndpointCreate, db: Session = Depends(get_db)):
    return crud_endpoint.create_endpoint(db, data)


@router.get("/", response_model=list[EndpointOut])
def list_endpoints(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_endpoint.get_endpoints(db, skip=skip, limit=limit)


@router.get("/{endpoint_id}", response_model=EndpointOut)
def read_endpoint(endpoint_id: int, db: Session = Depends(get_db)):
    endpoint = crud_endpoint.get_endpoint(db, endpoint_id)
    if endpoint is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    return endpoint


@router.put("/{endpoint_id}", response_model=EndpointOut)
def update_endpoint(endpoint_id: int, data: EndpointUpdate, db: Session = Depends(get_db)):
    endpoint = crud_endpoint.update_endpoint(db, endpoint_id, data)
    if endpoint is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    return endpoint


@router.delete("/{endpoint_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_endpoint(endpoint_id: int, db: Session = Depends(get_db)):
    endpoint = crud_endpoint.delete_endpoint(db, endpoint_id)
    if endpoint is None:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    return None