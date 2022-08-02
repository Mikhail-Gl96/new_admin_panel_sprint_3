## If it is your first try of this project

Run compose and other scripts below

## Build and run docker-compose.yml

```shell
docker-compose down && docker-compose build --no-cache && docker-compose up
```

## Create DB tables if not exists

```shell
PGPASSWORD=123qwe psql -h 0.0.0.0 -p 5435 -U app -d movies_database -f movies_database.sql
```

Or run script: `setup_scripts/create_db.sh`

## Upload data from Sqlite to postgres

```shell
cd ./sqlite_to_postgres
python3 load_data.py
```

Run file, wait few minutes, relax.

## Django locales

Run `create_django_locales.sh` to create locale files. <br>
Run `accept_django_locales.sh` to compile locale files in "django locale files". <br>

## Django migrations

Run `create_django_migration.sh` to create migration. <br>
Run `run_django_migrations.sh` to start django migrations. <br>
Use ```--fake``` и ```--fake-initial``` args to skip some or all migrations.

## Collect django static

Already included in app dockerfile

```shell
cd ./app
python manage.py collectstatic --no-input
```

## Create django super user

Replace: <br>
`$DJANGO_SUPERUSER_USERNAME` -> `SUPERUSER_USERNAME` <br>
`$DJANGO_SUPERUSER_EMAIL` -> `SUPERUSER_EMAIL` <br>
`$DJANGO_SUPERUSER_PASSWORD` -> `SUPERUSER_PASSWORD` <br>

```shell 
cd ./app
echo "from django.contrib.auth.models import User; User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME','$DJANGO_SUPERUSER_EMAIL','$DJANGO_SUPERUSER_PASSWORD')" | python manage.py shell
```

Or run script: `setup_scripts/create_django_super_user.sh`


# Elastic

## Run elastic in compose

Docker run
```shell
docker run -p 9200:9200 -e "discovery.type=single-node" -e ES_JAVA_OPTS="-Xms200m -Xmx200m" docker.elastic.co/elasticsearch/elasticsearch:7.7.0
```
Already included in project docker-compose file


## Help

If port is already in use - kill it. <br>
port 8123 as example

```shell
kill -9 $(lsof -i:8123 -t) 2> /dev/null
```

Run local server: `run_django_server_locally.sh`
