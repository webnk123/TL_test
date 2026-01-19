FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1


RUN apt update && apt -y install nano

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt


COPY . /code/

CMD ["/bin/bash", "-c", "\
    python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn --reload -w 4 djangoproj.wsgi:application -b 0.0.0.0:8000"]
