FROM python:3.13.0a2-bookworm

WORKDIR /RossLogApp

COPY . /RossLogApp/

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["flask", "run"]