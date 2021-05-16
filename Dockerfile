FROM python:3.8.2
ADD . /neuro
WORKDIR /neuro
RUN pip3 install -r requirements.txt