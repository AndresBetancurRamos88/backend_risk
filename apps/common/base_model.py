from datetime import datetime

from pytz import timezone
from sqlalchemy import Column, DateTime, Integer

from apps.extensions import db

UTC = timezone("America/Bogota")


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(), default=datetime.now(UTC))
    updated_at = Column(DateTime(), onupdate=datetime.now(UTC))
