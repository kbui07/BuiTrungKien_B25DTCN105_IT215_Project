from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CampaignTaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: str


class CampaignTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None
    priority: Optional[str] = None


class CampaignTaskAssign(BaseModel):
    assignee_id: int