FROM ubuntu
RUN apt-get update
RUN apt-get install python3 pip
RUN pip install -r requirements.txt
