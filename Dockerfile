FROM python:3.8

WORKDIR /app

ADD . /app

RUN apt update && apt upgrade -y
RUN apt install libffi-dev liblzma-dev
RUN pip install --upgrade pip
RUN pip install virtualenv
RUN pip install -r requirements.txt
RUN pip install -e .
RUN python /app/fusebox/manage.py collectstatic --noinput
RUN python /app/fusebox/manage.py migrate

EXPOSE 4000

ENV PYTHONPATH $PYTHONPATH:/app/fusebox

CMD ["gunicorn", "-b", "0.0.0.0:4000", "--timeout", "60", "--chdir", "/app/fusebox/fusebox", "--pythonpath", "/app/fusebox", "--reload", "wsgi:application"]
