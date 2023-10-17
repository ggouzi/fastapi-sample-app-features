FROM python:latest
WORKDIR /code/app
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./api /code/app/api
COPY ./cron /code/app/cron
COPY ./crud /code/app/crud
COPY ./db /code/app/db
COPY ./exceptions /code/app/exceptions
COPY ./models /code/app/models
COPY ./repository /code/app/repository
COPY ./schemas /code/app/schemas
COPY ./static /code/app/static
COPY ./test /code/app/test
COPY ./utils /code/app/utils
COPY ./main.py /code/app/main.py
COPY ./settings.py /code/app/settings.py
COPY ./.env.docker-compose /code/app/.env.docker-compose

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
