FROM python:3.8

COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY fit_action_example.py /app/fit_action_example.py

WORKDIR /app

ENTRYPOINT ["python", "fit_action_example.py"]