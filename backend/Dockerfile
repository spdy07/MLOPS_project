FROM python:3.9
RUN apt-get update && apt-get install -y python3 && apt-get install -y python3-pip
WORKDIR /home/user
COPY requirements.txt requirements.txt
COPY api.py api.py
COPY models models
COPY ./datas/ ./datas
RUN pip3 install -r requirements.txt
CMD python3 api.py --port 3000