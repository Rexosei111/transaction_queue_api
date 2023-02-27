from pydantic import BaseModel


class StatusModelBase(BaseModel):
    detail: str


class StatusModel400(StatusModelBase):
    status_code: int = 400


class StatusModel401(StatusModelBase):
    status_code: int = 401


class StatusModel404(StatusModelBase):
    status_code: int = 400
