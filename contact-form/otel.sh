OTEL_RESOURCE_ATTRIBUTES=service.name=com.github.rhildred.INFO8985_microservice_analysis,service.version=de732a0 \
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318 \
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf \
OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \
OTEL_EXPORTER_OTLP_INSECURE=true \
opentelemetry-instrument \
  --traces_exporter otlp \
  --metrics_exporter otlp \
  --logs_exporter otlp \
  uvicorn app:app --host 0.0.0.0 --port 5002
