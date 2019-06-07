FROM python:3.7

WORKDIR /app

ADD . /app

RUN apt update && apt upgrade -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -e .
RUN python /app/fusebox/manage.py collectstatic --noinput

EXPOSE 4000

ENV PYTHONPATH $PYTHONPATH:/app/fusebox

CMD ["gunicorn", "-b", "0.0.0.0:4000", "--timeout", "60", "--chdir", "/app/fusebox/fusebox", "--pythonpath", "/app/fusebox", "--reload", "wsgi:application"]
