FROM python:3.6-slim

WORKDIR /app

ADD . /app

RUN pip install -r /app/requirements.txt
RUN python fusebox/manage.py collectstatic -c --noinput
 
EXPOSE 4011

ENV PYTHONPATH $PYTHONPATH:/app/fusebox

CMD ["gunicorn", "-b", "0.0.0.0:4011", "--chdir", "/app/fusebox/fusebox", "wsgi:application"]
