FROM nginx/unit:1.29.0-python3.11

WORKDIR /app/api

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y python3-pip

RUN pip install virtualenv

RUN virtualenv /opt/api-env --python=python3

#RUN source /opt/api-env/bin/activate
RUN . /opt/api-env/bin/activate

COPY . .

COPY  config.json /docker-entrypoint.d/

ENV PATH="/opt/api-env/bin:$PATH"

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

EXPOSE 8000






