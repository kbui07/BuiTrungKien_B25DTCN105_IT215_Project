from pydantic import BaseModel, ConfigDict


class CampaignMemberBase(BaseModel):
    campaign_id: int
    user_id: int
    role: str


class CampaignMemberCreate(CampaignMemberBase):
    pass


class CampaignMemberUpdate(BaseModel):
    role: str


class CampaignMemberResponse(CampaignMemberBase):
    model_config = ConfigDict(from_attributes=True)