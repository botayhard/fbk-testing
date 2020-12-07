FROM python:latest

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY process.py .
CMD sleep 10 && python process.py
