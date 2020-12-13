FROM python:3.6-slim as base

RUN apt-get update -qq \
 && apt-get install -y --no-install-recommends \
    # required by psycopg2 at build and runtime
    libpq-dev \
     # required for health check
    curl \
 && apt-get autoremove -y

FROM base as builder

RUN apt-get update -qq && \
  apt-get install -y --no-install-recommends \
  build-essential \
  wget \
  openssh-client \
  graphviz-dev \
  pkg-config \
  git-core \
  openssl \
  libssl-dev \
  libffi6 \
  libffi-dev \
  libpng-dev

RUN pip install flask gunicorn pymystem3 rasa==2.1.2 rasa-core-sdk==0.14.0 rasa-sdk==2.1.2

RUN pip install -U spacy && \
  python -m spacy download xx_ent_wiki_sm &&\
  python -m spacy link xx_ent_wiki_sm xx

COPY . /app

WORKDIR /app

RUN echo '#!/bin/bash \n\n\
rasa run actions --quiet &\n\
rasa run -m models --enable-api --quiet &\n\
FLASK_APP=app.py; flask run --host=0.0.0.0 --port=$PORT\n' > /usr/bin/run.sh \
&& chmod +x /usr/bin/run.sh

ENTRYPOINT ["/usr/bin/run.sh"]