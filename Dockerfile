FROM python:3.9.7-slim-buster

ADD . /
RUN pip3 install -r requirements.txt
EXPOSE 8050
CMD ["python3", "./run_website.py"]
