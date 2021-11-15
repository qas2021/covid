FROM python:3.8.0-buster
WORKDIR /venv
ADD . /venv
EXPOSE 8000
COPY . /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt