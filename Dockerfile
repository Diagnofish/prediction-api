<<<<<<< HEAD
FROM python:3.10-slim
=======
FROM python:3.9
>>>>>>> ccbe819b735bc1a55a26288b359b8f0f40798ee7

ENV PYTHONBUFFERED True

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . ./

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
