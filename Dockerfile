FROM python:3.12.8-alpine3.21

EXPOSE 8080

WORKDIR /app

RUN pip install uv && uv sync

COPY api/database/conn.py .

CMD [ "uv", "run", "api/database/conn.py" ]
