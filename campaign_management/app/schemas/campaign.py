from pydantic import BaseModel, ConfigDict, Field


class CampaignBase(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None


class CampaignResponse(CampaignBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)