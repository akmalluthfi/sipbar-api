from fastapi import APIRouter
from fastapi import APIRouter
from app.core.db import SessionDep
from app.schemas.investment_record import InvestmentRecord
from sqlmodel import select, func, desc, distinct, extract
from app.utils.main import response
from app.utils.types import DefaultYear

router = APIRouter(prefix="/records", tags=["records"])


@router.get("/cards")
def cards(session: SessionDep, year: int = DefaultYear):
    query = select(
        func.count(distinct(InvestmentRecord.department)).label("department_count"),
        func.sum(InvestmentRecord.quantity).label("total_usage_item"),
    ).where(InvestmentRecord.year == year)

    results = session.exec(query).one()

    return {"department_count": results[0], "total_usage_item": results[1]}


@router.get("/top-item")
def top_item(session: SessionDep, limit: int = 10, year: int = DefaultYear):
    query = (
        select(InvestmentRecord.item, func.count().label("count"))
        .where(InvestmentRecord.year == year)
        .group_by(InvestmentRecord.item)
        .order_by(desc("count"))
        .limit(limit)
    )

    results = session.exec(query).all()

    return response(results, key1="item", key2="count")


@router.get("/item-trend")
def item_trend(session: SessionDep, year: int = DefaultYear):
    query = (
        select(
            extract("month", InvestmentRecord.date).label("month"),
            func.count(InvestmentRecord.date),
        )
        .where(InvestmentRecord.year == year)
        .group_by(extract("month", InvestmentRecord.date))
        .order_by(extract("month", InvestmentRecord.date))
    )

    results = session.exec(query).all()

    return response(results, key1="month", key2="count")


@router.get("/item-dist")
def item_dist(session: SessionDep, limit: int = 200, year: int = DefaultYear):
    query = (
        select(
            InvestmentRecord.department,
            func.count(InvestmentRecord.quantity).label("item_usage"),
        )
        .where(InvestmentRecord.year == year)
        .group_by(InvestmentRecord.department)
        .order_by(desc("item_usage"))
        .limit(limit)
    )

    results = session.exec(query).all()

    return response(results, key1="month", key2="count")
