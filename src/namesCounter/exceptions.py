from pydantic import BaseModel


class StatusModelBase(BaseModel):
    detail: str


class StatusModel400(StatusModelBase):
    codestatus: int = 400


class StatusModel401(StatusModelBase):
    codestatus: int = 401


class StatusModel404(StatusModelBase):
    codestatus: int = 404
