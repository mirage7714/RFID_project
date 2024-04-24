FROM ubuntu
RUN apt-get update
RUN yes | apt-get install python3 pip
RUN pip install -r requirements.txt
