from fastapi import APIRouter, HTTPException
from app.core.db import SessionDep
from app.schemas.investment_record import (
    InvestmentRecord,
    Item,
    PaginatedItem,
    Forecast,
    Metric,
    ForecastResponse,
)
from sqlmodel import select, func
import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

router = APIRouter(prefix="/records", tags=["records"])


@router.get("/items", response_model=PaginatedItem)
def items(session: SessionDep, q: str | None = None, page: int = 1) -> PaginatedItem:
    limit = 10
    offset = (page - 1) * limit

    # Build Base Query
    base_query = (
        select(
            InvestmentRecord.item,
            InvestmentRecord.item_code,
            func.count(InvestmentRecord.item).label("total_count"),
        )
        .group_by(InvestmentRecord.item, InvestmentRecord.item_code)
        .having(func.count(InvestmentRecord.item) >= 10)
    )

    if q:
        base_query = base_query.where(InvestmentRecord.item.ilike(f"%{q}%"))

    # Get parameter for pagination
    count_query = select(func.count()).select_from(base_query.subquery())
    total = session.exec(count_query).one()
    total_pages = (total + limit - 1) // limit if total > 0 else 0

    # Fetch the data
    paginated_query = base_query.offset(offset).limit(limit)
    results = session.exec(paginated_query).all()
    items = [Item(item_code=r.item_code, item=r.item) for r in results]

    return PaginatedItem(
        data=items,
        page=page,
        per_page=limit,
        total=total,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1,
    )


@router.get("/predict", response_model=ForecastResponse)
def predict(session: SessionDep, item: str):
    query = select(
        InvestmentRecord.item, InvestmentRecord.date, InvestmentRecord.quantity
    ).where(InvestmentRecord.item == item)
    results = session.exec(query).all()

    if not results:
        raise HTTPException(status_code=404, detail="Item Not Found")

    # Data Frame
    df = pd.DataFrame(results, columns=["item", "date", "quantity"])
    df["date"] = pd.to_datetime(df["date"])

    semester_usage = (
        df.resample("2QE", on="date")["quantity"]
        .sum()
        .reset_index()
        .rename(columns={"date": "ds", "quantity": "y"})
    )

    if len(semester_usage.index) < 6:
        raise HTTPException(status_code=400, detail="Not Enough Item")

    # Modeling & Predict
    model = Prophet()
    model.fit(semester_usage)
    future = model.make_future_dataframe(periods=2, freq="2Q")
    forecast = model.predict(future)

    # Evaluate
    compare = semester_usage[["ds", "y"]].merge(
        forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]], on="ds", how="left"
    )
    mae = mean_absolute_error(compare["y"], compare["yhat"])
    rmse = root_mean_squared_error(compare["y"], compare["yhat"])

    data = [
        Forecast(**row)
        for row in forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_dict(
            orient="records"
        )
    ]

    return ForecastResponse(metrics=Metric(mae=mae, rmse=rmse), data=data)
