FROM python:3.11-slim-bookworm

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

# Create a new user with UID 10016
RUN addgroup --gid 10016 choreo && \
    adduser --disabled-password --no-create-home --uid 10016 --ingroup choreo choreouser

# Switch to the new user
USER 10016

# Ekspos port default FastAPI
EXPOSE 8000

# CMD ["fastapi", "run", "app/main.py", "--port", "80"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]