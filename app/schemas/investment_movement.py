from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4


class InvestmentMovement(SQLModel, table=True):
    __tablename__: str = "investment_movements"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    item_code: str
    item: str
    opening_stock: int
    stock_in: int
    stock_out: int
    net_stock_change: int
    closing_stock: int
    closing_value: int
    year: int
    priority_category: str
    cluster_category: str
