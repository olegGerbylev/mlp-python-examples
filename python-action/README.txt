To install private requirements locally, create a file:

    ~/.config/pip/pip.conf

with a content:

    [global]
    index-url = https://<user>:<password>@nexus.just-ai.com/repository/pypi-all/simple

To build a docker image use command:

    docker build . -t action-example --build-arg NEXUS_USER=<user> --build-arg NEXUS_PASSWORD=<password>

To run docker image locally:

    docker run --network=host -e CAILA_URL=localhost:10601 -e CAILA_TOKEN=8974598357943 python-action