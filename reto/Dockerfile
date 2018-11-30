FROM python:3

ENV BIND_PORT 8000 
ENV POSTGRES_HOST localhost
ENV POSTGRES_PORT 5432

ADD . .
WORKDIR .


RUN pip install -r /requirements.txt

EXPOSE $BIND_PORT

CMD [ "python", "manage.py","migrate" ]

