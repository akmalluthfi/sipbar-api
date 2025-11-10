from fastapi import APIRouter, HTTPException, UploadFile
from app.core.db import SessionDep
from app.schemas.investment_record import InvestmentRecord
from app.schemas.investment_movement import InvestmentMovement
import pandas as pd
import io

router = APIRouter(prefix="/upload", tags=["upload"])

RECORDS_COLUMNS = [
    "document_number",
    "date",
    "item_code",
    "item",
    "quantity",
    "department",
    "year",
]

MOVEMENTS_COLUMNS = [
    "item_code",
    "item",
    "opening_stock",
    "stock_in",
    "stock_out",
    "net_stock_change",
    "closing_stock",
    "closing_value",
    "year",
]


@router.post("/records")
async def records(session: SessionDep, file: UploadFile):

    if file.content_type != "text/csv":
        raise HTTPException(422, "The uploaded file must be a csv file.")

    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))

        if list(df.columns) != RECORDS_COLUMNS:
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Invalid columns. Expected columns are {RECORDS_COLUMNS}, "
                    f"but got {list(df.columns)}."
                ),
            )

        for _, row in df.iterrows():
            row = row.to_dict()
            record = InvestmentRecord(**row)
            session.add(record)

        session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something wrong : {str(e)}")

    return {
        "status": "success",
        "summary": {
            "filename": file.filename,
            "rows": len(df),
            "columns": list(df.columns),
            "shape": df.shape,
        },
    }


@router.post("/movements")
async def movements(session: SessionDep, file: UploadFile):
    if file.content_type != "text/csv":
        raise HTTPException(422, "The uploaded file must be a csv file.")

    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))

        if list(df.columns) != MOVEMENTS_COLUMNS:
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Invalid columns. Expected columns are {MOVEMENTS_COLUMNS}, "
                    f"but got {list(df.columns)}."
                ),
            )

        for _, row in df.iterrows():
            row = row.to_dict()
            movement = InvestmentMovement(**row)
            session.add(movement)

        session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something wrong : {str(e)}")

    return {
        "status": "success",
        "summary": {
            "filename": file.filename,
            "rows": len(df),
            "columns": list(df.columns),
            "shape": df.shape,
        },
    }
