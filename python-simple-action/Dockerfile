FROM python:3.8

RUN mkdir $HOME/.ssh && chmod 700 $HOME/.ssh
RUN ssh-keyscan -H gitlab.just-ai.com >> $HOME/.ssh/known_hosts

RUN --mount=type=ssh pip install git+ssh://git@gitlab.just-ai.com/mpl-public/mpl-python-sdk.git@separate-sdk#mpl_sdk

RUN mkdir app

COPY simple_action_example.py /app
WORKDIR /app

ENTRYPOINT ["python", "simple_action_example.py"]