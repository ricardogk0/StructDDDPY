from sqlalchemy import Column, String, DateTime, Boolean
from datetime import datetime


class EntityBaseMapping:
    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    created_by_user = Column(String, nullable=False, default="system")
    updated_at = Column(DateTime, nullable=True)
    updated_by_user = Column(String, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
