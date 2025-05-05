###############################################################################################
# World Bank Data Analysis - Base
###############################################################################################
FROM python:3.13.3 as levell-wbda-base

RUN mkdir -p /app/

WORKDIR /app

RUN apt-get update
RUN apt-get install vim -y
RUN apt-get install net-tools -y
RUN apt-get install dos2unix -y
RUN apt-get install -y \
    git

###############################################################################################
# World Bank Data Analysis - TRAINING
###############################################################################################
FROM levell-wbda-base as levell-wbda-train

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Load Spacy
RUN python -m spacy download en_core_web_md

COPY ./src /app/

CMD [ "python", "main.py" ]
