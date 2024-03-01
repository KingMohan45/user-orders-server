FROM python:3.10.6

WORKDIR /server

COPY ./requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD exec make start