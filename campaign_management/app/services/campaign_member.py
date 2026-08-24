from sqlalchemy.orm import Session

from app.models.campaign import Campaign
from app.models.campaign_member import CampaignMember
from app.models.user import User
from app.core.exceptions import forbidden


def check_owner(db: Session, campaign_id: int, current_user: User):
    member = db.query(CampaignMember).filter(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.user_id == current_user.id,
            CampaignMember.role == "OWNER"
        ).first()

    if not member:
        raise forbidden("Chỉ OWNER mới có quyền")

    return member


def add_member(db: Session, campaign_id: int, user_id: int, current_user: User):
    check_owner(db, campaign_id, current_user)

    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    if not campaign:
        raise forbidden("Chiến dịch không tồn tại")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise forbidden("Người dùng không tồn tại")

    member = db.query(CampaignMember).filter(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.user_id == user_id
        ).first()

    if member:
        raise forbidden("Người dùng đã là thành viên")

    member = CampaignMember(
        campaign_id=campaign_id,
        user_id=user_id,
        role="MEMBER"
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member


def get_members(db: Session, campaign_id: int, current_user: User):
    member = db.query(CampaignMember).filter(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.user_id == current_user.id
        ).first()

    if not member:
        raise forbidden("Bạn không phải thành viên")

    return db.query(CampaignMember).filter(CampaignMember.campaign_id == campaign_id).all()


def delete_member(db: Session, campaign_id: int, user_id: int, current_user: User):
    check_owner(db, campaign_id, current_user)

    member = db.query(CampaignMember).filter(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.user_id == user_id
        ).first()

    if not member:
        raise forbidden("Người dùng không phải thành viên")

    if member.role == "OWNER":
        owner_count = db.query(CampaignMember).filter(
                CampaignMember.campaign_id == campaign_id,
                CampaignMember.role == "OWNER"
            ).count()

        if owner_count <= 1:
            raise forbidden("Không được xóa OWNER cuối cùng")

    db.delete(member)
    db.commit()

    return {
        "message": "Xóa thành viên thành công"
    }