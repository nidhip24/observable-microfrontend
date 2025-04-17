# Base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy app code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir \
        opentelemetry-distro \
        opentelemetry-exporter-otlp \
        opentelemetry-instrumentation-fastapi \
        opentelemetry-instrumentation-logging \
        opentelemetry-sdk

# Set environment variables for OpenTelemetry
ENV OTEL_SERVICE_NAME=ca.nk.contactform \
    OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318 \
    OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf \
    OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \
    OTEL_EXPORTER_OTLP_INSECURE=true

# Run with OpenTelemetry instrumentation
CMD ["opentelemetry-instrument", \
     "--traces_exporter=otlp", \
     "--logs_exporter=otlp", \
     "--metrics_exporter=otlp", \
     "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5002"]
