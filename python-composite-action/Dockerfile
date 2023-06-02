FROM python:3.8

COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY composite_action_example.py /app/composite_action_example.py

WORKDIR /app

ENTRYPOINT ["python", "composite_action_example.py"]