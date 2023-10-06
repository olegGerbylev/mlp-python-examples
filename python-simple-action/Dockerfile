FROM python:3.9

RUN pip install rayoptics==0.8.5
RUN pip install git+https://git@github.com/just-ai/mlp-python-sdk.git@dev

COPY simple_action_example.py /app/simple_action_example.py
WORKDIR /app

ENTRYPOINT ["python", "simple_action_example.py"]