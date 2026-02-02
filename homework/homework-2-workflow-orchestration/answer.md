# Module 2 Homework:
For this homework, we continue to using the same data , and extend for 2021 data.

## Question 1. Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size (i.e. the output file yellow_tripdata_2020-12.csv of the extract task)?
for this, i add a command at the extract task, for print file size :

```yaml
- id: extract
    type: io.kestra.plugin.scripts.shell.Commands
    outputFiles:
      - "*.csv"
    taskRunner:
      type: io.kestra.plugin.core.runner.Process
    commands:
      - wget -qO- https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{{inputs.taxi}}/{{render(vars.file)}}.gz | gunzip > {{render(vars.file)}}
      - ls -al --block-size=MB {{render(vars.file)}}
```
The result is 135MB (134.5 MiB)

## Question 2. What is the rendered value of the variable file when the inputs taxi is set to green, year is set to 2020, and month is set to 04 during execution?
variable file is :
"{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv"

rendered value is a value after inputs added to the variable.
So answer is : green_tripdata_2020-04.csv

## Question 3. How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?
After running all using Backfill executions at the scheduled Flow, and then see at the database using query :
```sql
select count(*) 
from yellow_tripdata
where filename like 'yellow_tripdata_2020%';
```
The result is 24648499

## Question 4. How many rows are there for the Green Taxi data for all CSV files in the year 2020?
After running all using Backfill executions at the scheduled Flow, and then see at the database using query :
```sql
select count(*) 
from green_tripdata
where filename like 'green_tripdata_2020%';
```
The result is 1734051

## Question 5. How many rows are there for the Yellow Taxi data for the March 2021 CSV file? 
After running all using Backfill executions at the scheduled Flow, and then see at the database using query :
```sql
select count(*) 
from yellow_tripdata
where filename like 'yellow_tripdata_2021-03%';
```
The result is 1925152

## Question 6. How would you configure the timezone to New York in a Schedule trigger? 
Add a timezone property set to America/New_York in the Schedule trigger configuration

```yaml
triggers:
  - id: green_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 1 * *"
    timezone: America/New_York
    inputs:
      taxi: green
```