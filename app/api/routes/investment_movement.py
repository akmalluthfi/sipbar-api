from fastapi import APIRouter
from fastapi import APIRouter
from app.core.db import SessionDep
from app.schemas.investment_movement import InvestmentMovement
from sqlmodel import select, func, desc, distinct, extract
from app.utils.main import response
from app.utils.types import DefaultYear

router = APIRouter(prefix="/movements", tags=["movements"])


@router.get("/cards")
def cards(session: SessionDep, year: int = DefaultYear):
    query = select(
        func.avg(InvestmentMovement.closing_value), func.count(InvestmentMovement.item)
    ).where(InvestmentMovement.year == year)

    results = session.exec(query).one()

    return {"avg_cost": results[0], "total_item": results[1]}


@router.get("/dist-cluster")
def dist_cluster(session: SessionDep):
    query = select(
        InvestmentMovement.cluster_category, func.count().label("count")
    ).group_by(InvestmentMovement.cluster_category)

    results = session.exec(query).all()

    return response(results, key1="cluster", key2="count")


@router.get("/priority-cluster")
def priority_cluster(session: SessionDep):
    query = select(
        InvestmentMovement.item,
        InvestmentMovement.stock_out,
        InvestmentMovement.closing_stock,
        InvestmentMovement.priority_category,
    )

    results = session.exec(query).all()

    return [
        {
            "item": item,
            "stock_out": stock_out,
            "closing_stock": closing_stock,
            "priority_category": priority_category,
        }
        for item, stock_out, closing_stock, priority_category in results
    ]
