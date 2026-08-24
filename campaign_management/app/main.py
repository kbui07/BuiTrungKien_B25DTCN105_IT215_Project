from fastapi import FastAPI

from app.db.database import Base, engine
import app.models
from app.routers import auth, user, campaign


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(campaign.router)


@app.get("/health")
def health_check():
    return {
        "message": "API đang hoạt động"
    }