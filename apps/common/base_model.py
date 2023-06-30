from apps.extensions import db
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func

from pytz import timezone
from datetime import datetime


UTC = timezone('America/Bogota')

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(), default=datetime.now(UTC))
    updated_at = Column(DateTime(), onupdate=datetime.now(UTC))