FROM python:3.11.0

# ENV PYTHONBUFFERED True

# ENV APP_HOME /app

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
