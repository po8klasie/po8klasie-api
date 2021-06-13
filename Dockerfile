FROM python:3.8

LABEL maintainer="mlazowik@gmail.com"

ENV PYTHONUNBUFFERED 1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt ./
RUN pip install -r requirements.txt

ENV SOURCE /opt/warsawlo
RUN mkdir -p $SOURCE
WORKDIR $SOURCE

COPY . .

RUN DJANGO_SECRET_KEY=fake DJANGO_ALLOWED_HOSTS=fake ./manage.py collectstatic --noinput

ENTRYPOINT ["/bin/sh", "-c"]

CMD ["sh /opt/warsawlo/entrypoint.sh"]
