FROM amd64/python:3.9-buster
RUN apt-get update && apt-get install -y python3 && apt-get install -y python3-pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
WORKDIR /home/user
COPY models models
COPY reports reports
COPY ./datas/ ./datas
COPY api.py api.py
CMD python3 api.py --port 3000