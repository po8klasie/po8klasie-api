# Comppile stage

FROM python:3.8-alpine AS compile-image

RUN apk update && apk add \
    g++ \
    linux-headers \
    make \
    postgresql-dev

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt ./
RUN pip install -r requirements.txt

# Final image stage

FROM python:3.8-alpine

LABEL maintainer="mlazowik@gmail.com"

RUN apk update && apk add \
    postgresql-dev

ENV PYTHONUNBUFFERED 1

COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

ENV SOURCE /opt/warsawlo
RUN mkdir -p $SOURCE
WORKDIR $SOURCE

COPY . .

RUN DJANGO_SECRET_KEY=fake DJANGO_ALLOWED_HOSTS=fake ./manage.py collectstatic --noinput

ENTRYPOINT ["/bin/sh", "-c"]

CMD ["sh /opt/warsawlo/entrypoint.sh"]
