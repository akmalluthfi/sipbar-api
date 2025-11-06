FROM python:3.11-slim-bookworm

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

# Buat user dengan UID dalam rentang yang direkomendasikan (misal: 10001)
RUN useradd -u 10001 appuser

# Jalankan sebagai user non-root dengan UID valid
USER 10001

# Ekspos port default FastAPI
EXPOSE 8000

# CMD ["fastapi", "run", "app/main.py", "--port", "80"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]