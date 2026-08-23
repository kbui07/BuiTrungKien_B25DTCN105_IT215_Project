from fastapi import HTTPException


def not_found(message: str):
    return HTTPException(
        status_code=404,
        detail={
            "status": "error",
            "message": message
        }
    )

def bad_request(message: str):
    return HTTPException(
        status_code=400,
        detail={
            "status": "error",
            "message": message
        }
    )

def forbidden(message: str):
    return HTTPException(
        status_code=403,
        detail={
            "status": "error",
            "message": message
        }
    )