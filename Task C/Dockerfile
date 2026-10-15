FROM continuumio/miniconda3

WORKDIR /app
COPY . /app

RUN conda env create -f env.yml
SHELL ["conda", "run", "-n", "tugas_4", "/bin/bash", "-c"]
RUN pip install -e .

ENV PYTHONUNBUFFERED=1