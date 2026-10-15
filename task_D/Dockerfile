FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir rns

COPY node_a.py node_b.py ./

CMD ["python", "node_b.py"]