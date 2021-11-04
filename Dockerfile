# FROM ubuntu
# RUN apt-get update
# RUN apt-get install software-properties-common
# RUN add-apt-repository ppa:deadsnakes/ppa
# RUN apt-get install python3-9
# RUN apt-get install python3-pip
# ADD code/ /
# RUN pip3 install -r requirements.txt
# EXPOSE 80
# CMD ['python3', './run_website.py']

FROM python:3.9.7-slim-buster

ADD . /
RUN pip3 install -r requirements.txt
EXPOSE 8050
CMD ["python3", "./run_website.py"]
