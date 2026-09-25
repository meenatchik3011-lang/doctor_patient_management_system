from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.patient import Patient
from app.models.user import User
from app.models.doctor import Doctor
from app.models.assignment import Assignment

from app.schemas.patient import (
    PatientCreate,
    PatientResponse
)

from app.auth.auth import (
    get_current_user,
    admin_required
)


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


# CREATE PATIENT
@router.post(
    "",
    response_model=PatientResponse
)
def create_patient(
    data: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    patient = Patient(
        name=data.name,
        age=data.age,
        phone=data.phone
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient


# GET ALL PATIENTS
@router.get(
    "",
    response_model=list[PatientResponse]
)
def get_patients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    patients = db.query(Patient).all()

    return patients


# GET SINGLE PATIENT
@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # Admin can view any patient
    if current_user.role == "admin":
        return patient

    # Doctor can view only assigned patients
    if current_user.role == "doctor":

        doctor = db.query(Doctor).filter(
            Doctor.user_id == current_user.id,
            Doctor.is_active == True
        ).first()

        if not doctor:
            raise HTTPException(
                status_code=403,
                detail="Doctor profile not found"
            )

        assignment = db.query(Assignment).filter(
            Assignment.doctor_id == doctor.id,
            Assignment.patient_id == patient_id
        ).first()

        if not assignment:
            raise HTTPException(
                status_code=403,
                detail="You can view only your assigned patients"
            )

        return patient

    raise HTTPException(
        status_code=403,
        detail="Access denied"
    )