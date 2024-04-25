FROM ubuntu
RUN apt-get update
RUN yes | apt-get install python3 pip
ADD . /home/root/web
RUN cd /home/root/web && pip install -r requirements.txt
CMD ['python /home/root/web/app.py']