
FROM python:3.12-slim

WORKDIR /app

# Create a dedicated non-root application user
RUN useradd --create-home --uid 1000 appuser

COPY src/ ./src/
COPY sample_logs/ ./sample_logs/

# Run the application without root privileges
USER appuser

CMD ["python", "src/log_analyser.py"]
