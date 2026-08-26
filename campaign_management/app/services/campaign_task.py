from sqlalchemy.orm import Session

from app.models.campaign_task import CampaignTask
from app.models.campaign import Campaign
from app.models.campaign_member import CampaignMember

from app.core.exceptions import bad_request, not_found, forbidden


VALID_STATUS = ["TODO", "IN_PROGRESS", "DONE"]
VALID_PRIORITY = ["LOW", "MEDIUM", "HIGH"]


def check_member(db: Session, campaign_id, user_id):
    member = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == user_id
    ).first()

    if not member:
        raise forbidden("Bạn không thuộc chiến dịch")

    return member


def create_task(db: Session, campaign_id, data, current_user):

    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    if not campaign:
        raise not_found("Không tìm thấy chiến dịch")

    check_member(db, campaign_id, current_user.id)

    if data.priority not in VALID_PRIORITY:
        raise bad_request("Invalid priority")

    task = CampaignTask(
        title=data.title,
        description=data.description,
        due_date=data.due_date,
        priority=data.priority,
        status="TODO",
        campaign_id=campaign_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_tasks(
    db: Session,
    campaign_id,
    current_user,
    status=None,
    priority=None,
    assignee_id=None,
    search=None,
    limit=10,
    offset=0
):

    check_member(db, campaign_id, current_user.id)

    query = db.query(CampaignTask).filter(CampaignTask.campaign_id == campaign_id)

    if status:
        if status not in VALID_STATUS:
            raise bad_request("Invalid status")

        query = query.filter(CampaignTask.status == status)

    if priority:
        if priority not in VALID_PRIORITY:
            raise bad_request("Invalid priority")

        query = query.filter(CampaignTask.priority == priority)

    if assignee_id:
        query = query.filter(CampaignTask.assignee_id == assignee_id)

    if search:
        query = query.filter(CampaignTask.title.like(f"%{search}%"))

    return query.offset(offset).limit(limit).all()


def get_task(db: Session, task_id, current_user):

    task = db.query(CampaignTask).filter(CampaignTask.id == task_id).first()

    if not task:
        raise not_found("Không tìm thấy đầu việc")

    check_member(db, task.campaign_id, current_user.id)

    return task


def update_task(db: Session, task_id, data, current_user):

    task = db.query(CampaignTask).filter(CampaignTask.id == task_id).first()

    if not task:
        raise not_found("Không tìm thấy đầu việc")

    member = check_member(db, task.campaign_id, current_user.id)
    if member.role != "OWNER":
            raise forbidden("Chỉ OWNER mới được xóa đầu việc")

    if data.status is not None:
        if data.status not in VALID_STATUS:
            raise bad_request("Invalid status")

        task.status = data.status

    if data.priority is not None:
        if data.priority not in VALID_PRIORITY:
            raise bad_request("Invalid priority")

        task.priority = data.priority

    if data.title is not None:
        task.title = data.title

    if data.description is not None:
        task.description = data.description

    if data.due_date is not None:
        task.due_date = data.due_date

    db.commit()
    db.refresh(task)

    return task


def delete_task(db: Session, task_id, current_user):

    task = db.query(CampaignTask).filter(CampaignTask.id == task_id).first()
    if not task:
        raise not_found("Không tìm thấy đầu việc")

    member = check_member(db, task.campaign_id, current_user.id)
    if member.role != "OWNER":
        raise forbidden("Chỉ OWNER mới được xóa đầu việc")

    db.delete(task)
    db.commit()

    return {
        "status": "success",
        "message": "Xóa đầu việc thành công"
    }


def assign_task(db: Session, task_id, data, current_user):
    task = db.query(CampaignTask).filter(CampaignTask.id == task_id).first()

    if not task:
        raise not_found("Không tìm thấy đầu việc")

    member = check_member(db, task.campaign_id, current_user.id)
    if member.role != "OWNER":
        raise forbidden("Chỉ OWNER mới được giao việc")

    assignee = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == task.campaign_id,
        CampaignMember.user_id == data.assignee_id
    ).first()

    if not assignee:
        raise bad_request("Nhân sự không thuộc chiến dịch")

    task.assignee_id = data.assignee_id

    db.commit()
    db.refresh(task)

    return task