FROM python:3.11.0-slim

WORKDIR /src

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get install -y libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY app /src/app 

EXPOSE 8000

CMD [ "uvicorn", "--host", "0.0.0.0","--port", "8000", "app.main:app"]

