FROM openjdk:17

RUN mkdir /app
WORKDIR /app

ADD target/mlp-random-search/lib    /app/lib
ADD target/mlp-random-search/*.jar        /app

ENTRYPOINT ["java", "-cp", "*:lib/*", "randomsearch.RandomSearchKt"]
