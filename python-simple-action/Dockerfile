FROM python:3.8

RUN pip install rayoptics==0.8.5
RUN pip install git+https://git@github.com/just-ai/mlp-python-sdk.git@dev
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y


COPY simple_action_example.py /app/simple_action_example.py
WORKDIR /app

ENTRYPOINT ["python", "simple_action_example.py"]