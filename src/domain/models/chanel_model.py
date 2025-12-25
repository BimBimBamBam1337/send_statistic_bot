from datetime import datetime
from .domain_model import DomainModel


class ChannelDomain(DomainModel):
    id: int
    name: str
    sheet_id: str
    created_at: datetime
