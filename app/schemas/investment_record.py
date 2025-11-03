from sqlmodel import Field, SQLModel
from pydantic import BaseModel
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


class Item(BaseModel):
    item_code: str
    item: str


class PaginatedItem(BaseModel):
    data: list[Item]
    page: int
    per_page: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool


class Forecast(BaseModel):
    ds: date
    yhat: float
    yhat_lower: float
    yhat_upper: float


class Metric(BaseModel):
    mae: float
    rmse: float


class ForecastResponse(BaseModel):
    metrics: Metric
    data: list[Forecast]
