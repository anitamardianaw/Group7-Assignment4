FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir pyzmq==26.2.1
COPY src/ /app/
ENV PYTHONUNBUFFERED=1
CMD ["python", "collector.py"]
