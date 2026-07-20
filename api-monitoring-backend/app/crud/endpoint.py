from sqlalchemy.orm import Session
from app.models.endpoint import Endpoint
from app.schemas.endpoint import EndpointCreate, EndpointUpdate


def create_endpoint(db: Session, data: EndpointCreate) -> Endpoint:
    new_endpoint = Endpoint(**data.model_dump())
    db.add(new_endpoint)
    db.commit()
    db.refresh(new_endpoint)
    return new_endpoint


def get_endpoint(db: Session, endpoint_id: int) -> Endpoint | None:
    return db.query(Endpoint).filter(Endpoint.id == endpoint_id).first()


def get_endpoints(db: Session, skip: int = 0, limit: int = 100) -> list[Endpoint]:
    return db.query(Endpoint).offset(skip).limit(limit).all()


def update_endpoint(db: Session, endpoint_id: int, data: EndpointUpdate) -> Endpoint | None:
    endpoint = get_endpoint(db, endpoint_id)
    if endpoint is None:
        return None

    for field, value in data.model_dump().items():
        setattr(endpoint, field, value)

    db.commit()
    db.refresh(endpoint)
    return endpoint


def delete_endpoint(db: Session, endpoint_id: int) -> Endpoint | None:
    endpoint = get_endpoint(db, endpoint_id)
    if endpoint is None:
        return None

    db.delete(endpoint)
    db.commit()
    return endpoint