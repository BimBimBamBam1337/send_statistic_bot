from datetime import datetime

from .domain_model import DomainModel


class UserDomain(DomainModel):
    id: int
    username: str
    is_admin: bool
    created_at: datetime
