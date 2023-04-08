# cyber-senior-project
###DB config
```
#if compose fails
docker run -d --name <container-name> --ulimit nofile=262144:262144 -p 8123:8123 clickhouse/<container-name>
```
###Table
```
docker exec -it <container-name> clickhouse-client


create database Analytics 

Use database Analytics

CREATE TABLE user_activity 
(
    `user_id` String,
    `post_id` String,
    `category` String,
    `likes` UInt8,
    `step_in` UInt8,
    `dbTime` DateTime MATERIALIZED now()
)
ENGINE = SummingMergeTree 
PARTITION BY toYYYYMMDD(dbTime)
ORDER BY (user_id, category)

insert into user_activity  SELECT generateUUIDv4(),1,2,3,4

```