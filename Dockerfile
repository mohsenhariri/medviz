FROM python:latest
WORKDIR /app
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
COPY . .

