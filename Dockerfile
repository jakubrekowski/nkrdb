FROM python:3.10.1-slim-buster

# pre-initialization
COPY ./src /src

# initialization
RUN pip install -r /src/requirements.txt
RUN cd /src
RUN python main.py