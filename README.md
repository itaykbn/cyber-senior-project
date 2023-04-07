# cyber-senior-project
###DB config
```
docker run -d --name clickhouse-server --ulimit nofile=262144:262144 -p 8123:8123 clickhouse/clickhouse-server
```
###Table
```
docker exec -it clickhouse-server clickhouse-client

CREATE TABLE Analytics.user_activity
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

insert into user_activity  SELECT generateUUIDv4(),1,2,3

```