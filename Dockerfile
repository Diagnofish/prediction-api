FROM python:3.9

ENV PYTHONBUFFERED True

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . ./

# Use a more flexible version of TensorFlow
RUN pip install --upgrade tensorflow

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
