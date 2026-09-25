from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

from app.schemas.auth import (
    RegisterRequest,
    TokenResponse
)

from app.auth.auth import (
    hash_password,
    verify_password,
    create_access_token
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# Register
@router.post(
    "/register",
    response_model=TokenResponse
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    # Check username
    existing_user = db.query(User).filter(
        User.username == data.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # Check email
    existing_email = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_email:
        raise HTTPException(
        status_code=400,
        detail="Email already exists"
        )

    # Check role
    if data.role not in ["admin", "doctor"]:
        raise HTTPException(
            status_code=400,
            detail="Role must be admin or doctor"
        )

    # Create user
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(
            data.password
        ),
        role=data.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Create JWT token
    token = create_access_token({
        "sub": user.username,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# Login
@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    # Find user
    user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Verify password
    if not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Create JWT token
    token = create_access_token({
        "sub": user.username,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
