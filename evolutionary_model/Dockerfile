FROM python:3.8


RUN pip install git+https://git@github.com/just-ai/mlp-python-sdk.git@dev
RUN pip install deap
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y


COPY simple_action_example.py /app/simple_action_example.py
WORKDIR /app

ENTRYPOINT ["python", "simple_action_example.py"]