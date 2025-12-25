from datetime import datetime
from typing import Optional
from .domain_model import DomainModel
from .chanel_model import ChannelDomain


class ExcelTableDomain(DomainModel):
    id: int
    name: str
    sheet_id: str
    sheet_url: str
    created_at: datetime
    channel: Optional[ChannelDomain] = None
