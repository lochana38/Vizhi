from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.setting import SettingCreate, SettingUpdate, SettingOut
from app.crud import setting as crud_setting

router = APIRouter(prefix="/settings", tags=["Settings"])


@router.post("/", response_model=SettingOut, status_code=status.HTTP_201_CREATED)
def create_setting(data: SettingCreate, db: Session = Depends(get_db)):
    return crud_setting.create_setting(db, data)


@router.get("/", response_model=list[SettingOut])
def list_settings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_setting.get_settings(db, skip=skip, limit=limit)


@router.get("/by-key/{key}", response_model=SettingOut)
def read_setting_by_key(key: str, db: Session = Depends(get_db)):
    setting = crud_setting.get_setting_by_key(db, key)
    if setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting


@router.get("/{setting_id}", response_model=SettingOut)
def read_setting(setting_id: int, db: Session = Depends(get_db)):
    setting = crud_setting.get_setting(db, setting_id)
    if setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting


@router.put("/{setting_id}", response_model=SettingOut)
def update_setting(setting_id: int, data: SettingUpdate, db: Session = Depends(get_db)):
    setting = crud_setting.update_setting(db, setting_id, data)
    if setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting


@router.delete("/{setting_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_setting(setting_id: int, db: Session = Depends(get_db)):
    setting = crud_setting.delete_setting(db, setting_id)
    if setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    return None
