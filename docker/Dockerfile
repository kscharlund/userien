FROM python:3.10
WORKDIR /opt/userien
COPY requirements.txt .
RUN apt update && apt install -y python3-dev libev-dev
RUN pip --disable-pip-version-check --no-cache-dir install -r requirements.txt
COPY src .
ENTRYPOINT ./server.py
