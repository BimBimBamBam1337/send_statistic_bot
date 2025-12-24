from datetime import datetime

from .domain_model import DomainModel


class ChannelDomain(DomainModel):
    id: int
    name: str
    created_at: datetime
