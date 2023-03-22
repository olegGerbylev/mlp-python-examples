FROM python:3.8

RUN mkdir $HOME/.ssh && chmod 700 $HOME/.ssh
RUN ssh-keyscan -H gitlab.just-ai.com >> $HOME/.ssh/known_hosts

COPY requirements.txt .
RUN --mount=type=ssh pip install -r ./requirements.txt

COPY fit_action_example.py /app/fit_action_example.py

WORKDIR /app

ENTRYPOINT ["python", "fit_action_example.py"]