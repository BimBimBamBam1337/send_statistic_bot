from datetime import datetime

from .domain_model import DomainModel


class ChanelDomain(DomainModel):
    id: int
    name: str
    created_at: datetime
