from pydantic import BaseModel, Field, ConfigDict


class TagSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(max_length=64)


class TagDBSchema(TagSchema):
    id: int
