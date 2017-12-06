FROM titomiguelcosta/fusebox:prod

WORKDIR /app

ADD . /app

RUN pip install -e .
RUN python /app/fusebox/manage.py collectstatic --noinput

EXPOSE 4000

ENV PYTHONPATH $PYTHONPATH:/app/fusebox

CMD ["gunicorn", "-b", "0.0.0.0:4000", "--timeout", "60", "--chdir", "/app/fusebox/fusebox", "--pythonpath", "/app/fusebox", "--reload", "wsgi:application"]
