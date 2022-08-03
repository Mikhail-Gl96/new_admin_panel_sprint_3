## Run postgres-elastic etl process local

```shell
cd ../
cd ./postgres_to_es/
python3 etl_process.py
```

## Load elastic search schema

Run script below to load es schema with curl

```shell
cd ../
cd ./postgres_to_es/etl_scripts
bash load_es_shema.sh
```

## Clear all elastic schemas

```shell
cd ../
cd ./postgres_to_es/etl_scripts
bash delete_etl_all_tables.sh
```

## Check elastic data for movies schema

```shell
cd ../
cd ./postgres_to_es/etl_scripts
bash common_etl_request.sh
```

