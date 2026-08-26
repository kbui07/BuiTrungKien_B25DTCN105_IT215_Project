from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.campaign_task import CampaignTaskCreate, CampaignTaskUpdate, CampaignTaskAssign
from app.services import campaign_task
from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/campaigns",
    tags=["Campaigns Task"]
)


@router.post("/campaigns/{campaign_id}/campaign-tasks")
def create_campaign_task(campaign_id: int, data: CampaignTaskCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return campaign_task.create_task(db, campaign_id, data, current_user)


@router.get("/campaigns/{campaign_id}/campaign-tasks")
def get_campaign_tasks(
    campaign_id: int,
    status: str = None,
    priority: str = None,
    assignee_id: int = None,
    search: str = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return campaign_task.get_tasks(
        db,
        campaign_id,
        current_user,
        status,
        priority,
        assignee_id,
        search,
        limit,
        offset
    )


@router.get("/campaign-tasks/{task_id}")
def get_campaign_task(task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return campaign_task.get_task(db, task_id,current_user)


@router.patch("/campaign-tasks/{task_id}")
def update_campaign_task(task_id: int, data: CampaignTaskUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return campaign_task.update_task(db, task_id, data, current_user)


@router.delete("/campaign-tasks/{task_id}")
def delete_campaign_task(task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return campaign_task.delete_task(db, task_id, current_user)


@router.patch("/campaign-tasks/{task_id}/assign")
def assign_campaign_task( task_id: int, data: CampaignTaskAssign, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return campaign_task.assign_task( db, task_id, data, current_user)