# To run using python
```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16
```
```bash
uv run python ingest_data.py \
  --pg_user=root \
  --pg_pass=root \
  --pg_host=localhost \
  --pg_port=5432 \
  --pg_db=ny_taxi \
  --targettable=yellow_taxi_trips
```
# To run using docker with same network
## Run PostgreSQL on the network
```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pgdatabase \
  postgres:16
```

## In another terminal, run pgAdmin on the same network
```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```
## In another terminal, run ingestion
```bash
docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --pg_user=root \
    --pg_pass=root \
    --pg_host=pgdatabase \
    --pg_port=5432 \
    --pg_db=ny_taxi \
    --targettable=yellow_taxi_trips
```
# To run using docker compose
```bash
docker-compose up
```

## In another terminal, run ingestion
```bash
docker run -it \
  --network=pipeline_default \
  taxi_ingest:v001 \
    --pg_user=root \
    --pg_pass=root \
    --pg_host=pgdatabase \
    --pg_port=5432 \
    --pg_db=ny_taxi \
    --targettable=yellow_taxi_trips
```
