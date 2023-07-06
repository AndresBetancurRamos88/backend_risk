from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

from apps.common.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    email = Column(EmailType(255), nullable=False, unique=True)
    given_name = Column(String(50), nullable=True)
    family_name = Column(String(50), nullable=True)
    risks_history = relationship(
        "RiskHistory", backref="users", cascade="all, delete")

    def __str__(self):
        return f"user {self.given_name}"
