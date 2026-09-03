from fastapi import HTTPException, status


def not_found(message: str):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "status": "error",
            "message": message
        }
    )

def bad_request(message: str):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "status": "error",
            "message": message
        }
    )

def unauthorized(message: str):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "status": "error",
            "message": message
        }
    )

def forbidden(message: str):
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
            "status": "error",
            "message": message
        }
    )


def too_many_requests(message: str):
    return HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail={
            "status": "error",
            "message": message
        }
    )