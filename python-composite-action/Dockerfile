FROM python:3.8

RUN mkdir $HOME/.ssh && chmod 700 $HOME/.ssh
RUN ssh-keyscan -H gitlab.just-ai.com >> $HOME/.ssh/known_hosts

COPY requirements.txt .
RUN --mount=type=ssh pip install -r ./requirements.txt

COPY composite_action_example.py /app/composite_action_example.py

WORKDIR /app

ENTRYPOINT ["python", "composite_action_example.py"]