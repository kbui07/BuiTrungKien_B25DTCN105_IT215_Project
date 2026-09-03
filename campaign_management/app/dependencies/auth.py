from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import forbidden, unauthorized
from app.db.database import get_db
from app.models.user import User

scheme = HTTPBearer() 

def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(scheme),
    db: Session = Depends(get_db)
):

    token = creds.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise unauthorized("Token không hợp lệ")

    except ExpiredSignatureError:
        raise unauthorized("Token đã hết hạn")

    except JWTError:
        raise unauthorized("Token không hợp lệ")

    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise forbidden("Người dùng không tồn tại")

    if not user.is_active:
        raise forbidden("Tài khoản không hoạt động")

    return user


def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise forbidden("Chỉ Admin mới có quyền")

    return current_user