FROM python:3.9

COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY simple_action_example.py /app/simple_action_example.py
WORKDIR /app

ENTRYPOINT ["python", "simple_action_example.py"]