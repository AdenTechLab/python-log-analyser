
FROM python:3.12-slim

WORKDIR /app

COPY src/ ./src/
COPY sample_logs/ ./sample_logs/

CMD ["python", "src/log_analyser.py"]
