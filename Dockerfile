FROM python:3.6

WORKDIR /app

ADD . /app

RUN pip install -r /app/requirements.txt
RUN python /app/fusebox/manage.py collectstatic -c --noinput

#EXPOSE 4000

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH $PYTHONPATH:/app/fusebox

CMD ["gunicorn", "-b", "0.0.0.0:4000", "--chdir", "/app/fusebox/fusebox", "--reload", "wsgi:application"]
