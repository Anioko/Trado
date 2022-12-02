FROM pypy:3.9 


# Packages required for psycopg2
RUN apt update && apt install  gcc musl-dev

WORKDIR /src


COPY ./requirements /src/requirements

RUN pip3 install -r ./requirements/dev.txt 

ENV PYTHONIOENCODING=UTF-8


COPY . /src

RUN ls

