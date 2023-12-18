FROM python:3.10-slim

ENV PYTHONBUFFERED True

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . ./

RUN pip install -r requirements.txt

# Definisikan fungsi Gunicorn untuk fleksibilitas nanti
ENV GUNICORN_CMD "exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 app:app"

# Gunakan GOOGLE_ENTRYPOINT jika tersedia, jika tidak default ke GUNICORN_CMD
ENV GOOGLE_ENTRYPOINT=${GOOGLE_ENTRYPOINT:-$GUNICORN_CMD}

# Gunakan "google_run_entrypoint" yang memanfaatkan GOOGLE_ENTRYPOINT
CMD ["google_run_entrypoint"]
