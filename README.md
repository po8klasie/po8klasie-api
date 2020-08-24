# WarsawLO BE

## Local development

Requirements:
- docker
- docker-compose

Copy an example `docker-compose.yml` file from: [warsawlo/infra](https://github.com/WarsawLO/infra/blob/master/docker-compose.yml) 
and paste it to the project's root directory. 

In the root directory create your `.env` file with variables:
```shell script
DB_USER=warsawlo
DB_PASSWORD=warsawlo
DB_NAME=warsawlo
```

In the `docker-compose.yml` change backend's env_file to your `.env` file's name. You might also want to set `DJANGO_DEBUG` to `"True"`.

#### Run
```shell script
docker-compose up -d --build # build and start containers

docker-compose exec web python manage.py migrate --noinput # run migrations
```

#### Linter
We use [black](https://github.com/psf/black) autoformatter and flake8. 

Install:
```shell script
pip install black # install
pip install flake8
```

Run:
```shell script
black .
flake8
```

## Queries

#### Boolean filtering
Besides normal URI syntax, you can also use OR's and AND's in GET requests.
For OR put a '|' (pipe) character between options, eg.:
```/api/subject/?high_school_class=&id=&name=pol|hist```
should return a list of all subjects with name either "pol", "hist" or "ang".

For AND just add the param once again with a new condition, eg:
```/api/school/?highschoolclass__extendedsubject__name=mat&highschoolclass__extendedsubject__name=fiz```
should return a list of all schools with classes that has both maths and physics as their extended subjects 

You can mix ORs and ANDs in the same request. OR has a higher precedence.

#### Ordering
Add an 'ordering=name_of_the_field'. For descending order, precede name of the field with a dash. You can also order by nested fields. Eg:
```/api/school/?ordering=school_type,-id```
should return a list of all schools, ordered by school type in ascending order, and by id in descending order.
