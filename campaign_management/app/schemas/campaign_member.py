from pydantic import BaseModel


class CampaignMemberCreate(BaseModel):
    user_id: int


class CampaignMemberResponse(BaseModel):
    user_id: int
    name: str
    email: str
    role: str