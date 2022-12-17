FROM python:3.8

WORKDIR /app

# 1. install whole list of dependencies except of caila-transport
COPY requirements.txt        /app
RUN grep -v "caila-transport" requirements.txt | xargs pip install

# 2. install caila_transport from wheel
COPY caila_transport-*.whl        /app
RUN pip install caila_transport-*.whl

COPY src      /app

ENTRYPOINT ["python", "ActionExample.py"]