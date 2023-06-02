FROM python:3.8

COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY rest_client_example.py /app/rest_client_example.py
WORKDIR /app

ENTRYPOINT ["python", "rest_client_example.py"]