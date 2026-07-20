from sqlalchemy.orm import Session
from app.models.setting import Setting
from app.schemas.setting import SettingCreate, SettingUpdate


def create_setting(db: Session, data: SettingCreate) -> Setting:
    new_setting = Setting(**data.model_dump())
    db.add(new_setting)
    db.commit()
    db.refresh(new_setting)
    return new_setting


def get_setting(db: Session, setting_id: int) -> Setting | None:
    return db.query(Setting).filter(Setting.id == setting_id).first()


def get_setting_by_key(db: Session, key: str) -> Setting | None:
    return db.query(Setting).filter(Setting.key == key).first()


def get_settings(db: Session, skip: int = 0, limit: int = 100) -> list[Setting]:
    return db.query(Setting).offset(skip).limit(limit).all()


def update_setting(db: Session, setting_id: int, data: SettingUpdate) -> Setting | None:
    setting = get_setting(db, setting_id)
    if setting is None:
        return None
    for field, value in data.model_dump().items():
        setattr(setting, field, value)
    db.commit()
    db.refresh(setting)
    return setting


def delete_setting(db: Session, setting_id: int) -> Setting | None:
    setting = get_setting(db, setting_id)
    if setting is None:
        return None
    db.delete(setting)
    db.commit()
    return setting
