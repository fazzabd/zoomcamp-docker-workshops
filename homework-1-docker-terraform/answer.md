# Module 1 Homework: Docker & SQL

## Question 1. Understanding Docker images
```bash
docker run -it --rm --entrypoint=bash python:3.13
```
and run :
```bash
pip --version
```
Answer is 25.3

## Question 2. Understanding Docker networking and docker-compose
hostname got from service name, and port use 5432 because both in the same docker network.
Answer is db:5432

## Question 3. Counting short trips
query :
```sql
SELECT count(*) FROM green_tripdata
where 
lpep_pickup_datetime between '2025-11-01' and '2025-12-01'  
and trip_distance<=1;
```
Answer is 8007

## Question 4. Longest trip for each day
query :
```sql
SELECT lpep_pickup_datetime FROM green_tripdata
where trip_distance<=100
order by trip_distance desc
limit 1;
```
Answer is 2025-11-14

## Question 5. Biggest pickup zone
query :
```sql
SELECT 
b.Zone as pickup_zone,
sum(total_amount) as total_amount
FROM green_tripdata a
left join taxi_zone_lookup b on a.PULocationID=b.LocationID
where lpep_pickup_datetime::date = '2025-11-18' 
group by 1
order by 2 desc
limit 1;
```
Answer is East Harlem North

## Question 6. Largest tip
query :
```sql
SELECT 
b.Zone as pickup_zone,
c.Zone as dropoff_zone,
a.*
FROM green_tripdata a
left join taxi_zone_lookup b on a.PULocationID=b.LocationID
left join taxi_zone_lookup c on a.DOLocationID=c.LocationID
where a.lpep_pickup_datetime BETWEEN '2025-11-01' and '2025-12-01' 
and b.Zone ='East Harlem North'
order by a.tip_amount desc
limit 1
;
```
Answer is Yorkville West

## Question 7. Terraform Workflow
1. Downloading the provider plugins and setting up backend -> terraform init
2. Generating proposed changes and auto-executing the plan -> terraform apply -auto-approve
3. Remove all resources managed by terraform -> terraform destroy
