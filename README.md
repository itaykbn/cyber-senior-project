# cyber-senior-project
###DB config
```
docker run -d --name clickhouse-server --ulimit nofile=262144:262144 -p 8123:8123 clickhouse/clickhouse-server
```
###Table
```
docker exec -it clickhouse-server clickhouse-client

CREATE TABLE test
(
    `user` String,
    `category` UInt8,
    `dbTime` DateTime MATERIALIZED now()
)
ENGINE = MergeTree
PARTITION BY toYYYYMMDD(dbTime)
ORDER BY (user, category)

insert into test  SELECT generateUUIDv4(),1

```