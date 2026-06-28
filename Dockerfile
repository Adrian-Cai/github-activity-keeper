FROM python:3.11-alpine

WORKDIR /app

RUN apk add --no-cache git openssh-client

COPY . .

RUN pip install --no-cache-dir pyyaml

ENTRYPOINT ["python", "-m", "keeper"]
