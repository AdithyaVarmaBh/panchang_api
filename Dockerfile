FROM python:3.11-slim

RUN pip install pyswisseph astral pytz fastapi uvicorn

COPY . /app
WORKDIR /app

CMD ["uvicorn", "main.app", "host", "0.0.0.0", "--port", "8000"]