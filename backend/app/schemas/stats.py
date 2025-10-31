from pydantic import BaseModel


class StatsResponse(BaseModel):
    projects: int
    members: int
    sessions: int
    devices: int