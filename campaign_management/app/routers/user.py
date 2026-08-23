from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user, require_admin
from app.models.user import User
from app.schemas.user import UserResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=list[UserResponse], dependencies=[Depends(require_admin)])
def get_users(
    name: str | None = None,
    email: str | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(User)

    if name:
        query = query.filter(User.full_name.contains(name))

    if email:
        query = query.filter(User.email.contains(email))

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    return query.all()