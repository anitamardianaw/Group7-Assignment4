FROM python:3.9-slim
WORKDIR /app
COPY environment.yml .
RUN pip install pyzmq
COPY . .