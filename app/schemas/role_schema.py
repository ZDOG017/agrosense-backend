from pydantic import BaseModel, ConfigDict


class RoleRead(BaseModel):
    role_id: int
    role_name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)
