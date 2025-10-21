from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4
from datetime import date


class InvestmentRecord(SQLModel, table=True):
    __tablename__: str = "investment_records"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    document_number: str
    date: date
    item_code: str
    item: str
    quantity: int
    department: str
    year: int
