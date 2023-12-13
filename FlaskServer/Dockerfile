FROM python:3.13.0a2-bookworm

WORKDIR /RossLog

COPY . /RossLog/

COPY .flaskenv /RossLog/

RUN pip install --progress-bar off -r requirements.txt

EXPOSE 5002

CMD ["flask", "run", "--debug"]