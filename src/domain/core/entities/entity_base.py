from datetime import datetime
from uuid import uuid4
from typing import Optional
from pydantic.v1 import BaseModel, Field


class EntityBase(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by_user: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_by_user: Optional[str] = None
    is_deleted: bool = False

    def set_updated(self, user: Optional[str] = None):
        self.updated_at = datetime.utcnow()
        if user:
            self.updated_by_user = user

    def toggle_deleted_status(self, user: Optional[str] = None):
        self.set_updated(user)
        self.is_deleted = not self.is_deleted

    class Config:
        arbitrary_types_allowed = True
