from sqlalchemy import Boolean, Column, DECIMAL, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from apps.common.base_model import BaseModel


class Risk(BaseModel):
    __tablename__ = 'risks'    
    risk = Column(String(50), nullable=True)
    status = Column(Boolean, default=True)
    risks_history = relationship("RiskHistory", backref="risks", cascade="all, delete")
    def __str__(self):
        return f"user {self.risk}"
    

class RiskHistory(BaseModel):
    __tablename__ = 'risks_history'
    title = Column(String(50), nullable=True)
    impact = Column(String(50), nullable=True)
    probability = Column(DECIMAL(precision=5, scale=2))
    description = Column(Text())
    risk_id = Column(Integer, ForeignKey('risks.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    def __str__(self):
        return f"risk impact {self.impact}"
