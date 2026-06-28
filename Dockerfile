FROM python:3.11-alpine

WORKDIR /app

RUN apk add --no-cache git openssh-client

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "-m", "app.main"]
