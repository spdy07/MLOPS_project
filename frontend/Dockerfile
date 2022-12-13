FROM python:3.9
RUN apt-get update && apt-get install -y python3 && apt-get install -y python3-pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
WORKDIR /home/user
COPY Main_page.py Main_page.py
COPY pages/ pages/
CMD streamlit run Main_page.py --server.port 8501