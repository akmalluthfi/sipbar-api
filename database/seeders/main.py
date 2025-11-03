import os
import logging
import pandas as pd
from pathlib import Path
from sqlmodel import Session
from datetime import datetime
from app.core.db import engine

from app.schemas.investment_record import InvestmentRecord
from app.schemas.investment_movement import InvestmentMovement

BASE_DIR = Path(os.path.dirname(__file__)) / "csv"

logging.basicConfig(
    filename=Path(os.path.dirname(__file__)) / "log.txt",
    filemode="w",
    level=logging.ERROR,
)


def convert_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()
    # return datetime.strptime(date_str, "%Y-%m-%d").date()
    # return date.strftime("%Y-%m-%d")


def insert_movements(session):
    df = pd.read_csv(BASE_DIR / "movements_rev.csv")

    for _, row in df.iterrows():
        row = row.to_dict()

        data = {
            "item_code": row["Kode"],
            "item": row["Uraian"],
            "opening_stock": row["Nilai_Jumlah"],
            "stock_in": row["Mutasi_Masuk"],
            "stock_out": row["Mutasi_Keluar"],
            "net_stock_change": row["Mutasi_Jumlah"],
            "closing_stock": row["Jumlah"],
            "closing_value": row["Rupiah"],
            "year": row["Tahun"],
            "priority_category": row["Prioritas"],
            "cluster_category": row["Flow_Category"],
        }

        movement = InvestmentMovement(**data)
        session.add(movement)

    session.commit()


def insert_records(session):
    df = pd.read_csv(BASE_DIR / "records.csv")
    for _, row in df.iterrows():
        row = row.to_dict()

        data = {
            "document_number": row["No Dokumen"],
            "date": convert_date(row["Tgl Dok"]),
            "item_code": row["Kode Barang"],
            "item": row["Nama Barang"],
            "quantity": row["Jumlah"],
            "department": row["Keterangan"],
            "year": row["Tahun"],
        }

        record = InvestmentRecord(**data)
        session.add(record)

    session.commit()


def seed():
    with Session(engine) as session:
        insert_movements(session)
        insert_records(session)


if __name__ == "__main__":
    print("SQL seeding started.")
    seed()
    print("SQL seeding completed.")
