from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.campaign import Campaign
from app.models.campaign_member import CampaignMember
from app.models.user import User
from app.core.exceptions import forbidden


def create_campaign(db: Session, data, current_user: User):
    campaign = Campaign(name=data.name, description=data.description, created_at=datetime.now(timezone.utc),owner_id=current_user.id)

    db.add(campaign)
    db.commit()
    db.refresh(campaign)

    member = CampaignMember(
        campaign_id=campaign.id,
        user_id=current_user.id,
        role="OWNER"
    )

    db.add(member)
    db.commit()

    return campaign


def get_campaigns(db: Session, current_user: User, search: str | None = None):
    query = db.query(Campaign).join(CampaignMember).filter(CampaignMember.user_id == current_user.id)

    if search:
        query = query.filter(Campaign.name.contains(search))

    return query.all()


def get_campaign(db: Session, campaign_id: int, current_user: User):
    member = db.query(CampaignMember).filter(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.user_id == current_user.id
        ).first()

    if not member:
        raise forbidden("Bạn không phải thành viên chiến dịch")

    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    if not campaign:
        raise forbidden("Chiến dịch không tồn tại")

    return campaign


def update_campaign(db: Session, campaign_id: int, data, current_user: User):
    member = db.query(CampaignMember).filter(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.user_id == current_user.id,
            CampaignMember.role == "OWNER"
        ).first()

    if not member:
        raise forbidden("Chỉ OWNER mới có quyền")

    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    if not campaign:
        raise forbidden("Chiến dịch không tồn tại")

    if data.name is not None:
        campaign.name = data.name

    if data.description is not None:
        campaign.description = data.description

    db.commit()
    db.refresh(campaign)

    return campaign


def delete_campaign(db: Session, campaign_id: int, current_user: User):
    member = db.query(CampaignMember).filter(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.user_id == current_user.id,
            CampaignMember.role == "OWNER"
        ).first()

    if not member:
        raise forbidden("Chỉ OWNER mới có quyền")

    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    if not campaign:
        raise forbidden("Chiến dịch không tồn tại")

    db.delete(campaign)
    db.commit()

    return {
        "message": "Xóa chiến dịch thành công"
    }