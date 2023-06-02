FROM python:3.8

COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY client_app_example.py /app/client_app_example.py

WORKDIR /app

ENTRYPOINT ["python", "client_app_example.py"]