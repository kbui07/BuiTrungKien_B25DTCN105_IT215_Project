from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.campaign import CampaignCreate, CampaignUpdate, CampaignResponse
from app.schemas.campaign_member import CampaignMemberCreate, CampaignMemberResponse
from app.services import campaign
from app.services import campaign_member
from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/campaigns",
    tags=["Campaigns"]
)


@router.post("",response_model=CampaignResponse)
def create_campaign(data: CampaignCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return campaign.create_campaign(db, data, current_user)


@router.get("",response_model=list[CampaignResponse])
def get_campaigns(search: str | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return campaign.get_campaigns(db, current_user, search)


@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign( campaign_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return campaign.get_campaign(db, campaign_id, current_user)


@router.put("/{campaign_id}", response_model=CampaignResponse)
def update_campaign(campaign_id: int, data: CampaignUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return campaign.update_campaign(db, campaign_id, data, current_user)


@router.delete("/{campaign_id}")
def delete_campaign(campaign_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return campaign.delete_campaign(db, campaign_id, current_user)


@router.post("/{campaign_id}/members", response_model=CampaignMemberResponse)
def add_member(campaign_id: int, data: CampaignMemberCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    member = campaign_member.add_member(db, campaign_id, data.user_id, current_user)

    return {
        "user_id": member.user_id,
        "name": member.user.full_name,
        "email": member.user.email,
        "role": member.role
    }


@router.get("/{campaign_id}/members", response_model=list[CampaignMemberResponse])
def get_members(campaign_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    members = campaign_member.get_members(db, campaign_id, current_user)
    return [
        {
            "user_id": member.user_id,
            "name": member.user.full_name,
            "email": member.user.email,
            "role": member.role
        }
        for member in members
    ]


@router.delete("/{campaign_id}/members/{user_id}")
def delete_member( campaign_id: int, user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return campaign_member.delete_member(db, campaign_id, user_id, current_user)