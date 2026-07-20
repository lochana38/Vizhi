from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SettingBase(BaseModel):
    key: str
    value: Optional[str] = None


class SettingCreate(SettingBase):
    pass


class SettingUpdate(SettingBase):
    pass


class SettingOut(SettingBase):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True
