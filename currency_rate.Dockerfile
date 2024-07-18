FROM python:3.11.8-alpine3.19

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update
RUN apk add file
RUN apk add git
RUN pip3 install uv

COPY pyproject.toml /app/pyproject.toml
COPY ./src/bot /app/src/bot

WORKDIR /app

RUN python3 -m uv pip install -e .
RUN apk del git

RUN crontab -l | { cat; echo "0 0 * * * currency-rate-cli --run --config currency_rate.toml"; } | crontab -

CMD cron