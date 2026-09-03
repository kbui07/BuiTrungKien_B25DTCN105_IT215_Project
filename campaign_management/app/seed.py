from app.db.database import SessionLocal
from app.models.user import User
from app.models.campaign import Campaign
from app.models.campaign_member import CampaignMember
from app.models.campaign_task import CampaignTask
from app.services.auth import hash_password


def seed_data():
    db = SessionLocal()

    try:
        user1 = User(
            email="owner@gmail.com",
            password_hash=hash_password("123456"),
            full_name="Owner",
            role="OWNER"
        )

        user2 = User(
            email="member1@gmail.com",
            password_hash=hash_password("123456"),
            full_name="Member 1",
            role="USER"
        )

        user3 = User(
            email="member2@gmail.com",
            password_hash=hash_password("123456"),
            full_name="Member 2",
            role="USER"
        )

        db.add_all([user1, user2, user3])
        db.commit()

        db.refresh(user1)
        db.refresh(user2)
        db.refresh(user3)

        campaign = Campaign(
            name="Campaign Demo",
            description="Chiến dịch dùng để test API",
            owner_id=user1.id
        )

        db.add(campaign)
        db.commit()
        db.refresh(campaign)

        member1 = CampaignMember(
            campaign_id=campaign.id,
            user_id=user2.id,
            role="CONTENT"
        )

        member2 = CampaignMember(
            campaign_id=campaign.id,
            user_id=user3.id,
            role="DESIGN"
        )

        db.add_all([member1, member2])
        db.commit()

        task1 = CampaignTask(
            title="Viết nội dung Facebook",
            description="Chuẩn bị nội dung cho bài đăng",
            status="TODO",
            priority="HIGH",
            campaign_id=campaign.id,
            assignee_id=user2.id
        )

        task2 = CampaignTask(
            title="Thiết kế banner",
            description="Thiết kế banner cho chiến dịch",
            status="IN_PROGRESS",
            priority="MEDIUM",
            campaign_id=campaign.id,
            assignee_id=user3.id
        )

        db.add_all([task1, task2])
        db.commit()

        print("Seed dữ liệu thành công!")
        print()
        print("Owner:")
        print("Email: owner@gmail.com")
        print("Password: 123456")
        print()
        print("Member 1:")
        print("Email: member1@gmail.com")
        print("Password: 123456")
        print()
        print("Member 2:")
        print("Email: member2@gmail.com")
        print("Password: 123456")

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()