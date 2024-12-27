from pydantic import BaseModel

class FactCreate(BaseModel):
    text: str

class FactResponse(BaseModel):
    id: int
    text: str

    class Config:
        orm_mode = True
