from datetime import datetime

from .domain_model import DomainModel


class ExcelTableDomain(DomainModel):
    id: int
    sheet_id: str
    sheet_url: str
    created_at: datetime
