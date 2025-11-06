FROM python:3.11-slim-bookworm

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

# Buat user non-root untuk keamanan
RUN adduser --disabled-password --gecos '' appuser

# Beralih ke user non-root
USER appuser

# Ekspos port default FastAPI
EXPOSE 8000

# CMD ["fastapi", "run", "app/main.py", "--port", "80"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]