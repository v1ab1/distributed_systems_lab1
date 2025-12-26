from pydantic import Field, BaseModel


class PersonResponseSchema(BaseModel):
    id: int
    name: str
    age: int | None = Field(None)
    address: str | None = Field(None)
    work: str | None = Field(None)

    class Config:
        from_attributes = True


class PersonCreateRequestSchema(BaseModel):
    name: str
    age: int | None = Field(None)
    address: str | None = Field(None)
    work: str | None = Field(None)
