from sqlalchemy import Column, Integer

from app.database import Base


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    doctor_id = Column(
        Integer,
        nullable=False
    )

    patient_id = Column(
        Integer,
        nullable=False
    )