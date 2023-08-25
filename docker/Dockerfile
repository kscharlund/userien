FROM python:3.10
WORKDIR /opt/userien
COPY requirements.txt .
RUN pip --disable-pip-version-check --no-cache-dir install -r requirements.txt
COPY . .
ENTRYPOINT ./server.py
