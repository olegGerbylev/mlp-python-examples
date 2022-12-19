FROM python:3.8

#RUN pip install git+ssh://git@gitlab.just-ai.com/mpl-public/mpl-python-sdk.git@separate-sdk#mpl_sdk

# TODO: ssh keys?
COPY requirements.txt        /app
RUN pip install -r requirements.txt

COPY src      /app
WORKDIR /app

ENTRYPOINT ["python", "ActionExample.py"]