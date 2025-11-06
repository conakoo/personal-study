# Iceberg

> Iceberg is a high-performance format for huge analytic tables. Iceberg brings the reliability and simplicity of SQL tables to big data, while making it possible for engines like Spark, Trino, Flink, Presto, Hive and Impala to safely work with the same tables, at the same time.

## Components
- Catalog layer: is for tracking the location of tables and views and identifying the current metadata file for a given table.
- Metadata layer: is composed of a hierachy of files (metadata files, manifest lists, and manifest files) that represent the state of an Iceberg table at different points in time.
- Data layer: holds the actual data files, such as those in Parquet or ORC formats.


```
                  ┌────────────┐
                  │ JupyterHub │
                  └──────┬─────┘
                         │
               ┌─────────▼──────────┐
               │       Spark        │
               │  (Iceberg Writer)  │
               └─────────┬──────────┘
                         │
         ┌───────────────▼───────────────┐
         │             Iceberg           │
         │       (Table Format Layer)    │
         ├────────────┬──────────────────┤
         │            │                  │
┌────────▼───────┐ ┌──▼──────────────┐   │
│Nessie/Gravitino│ │  Object Store   │   │
│ (Catalog)      │ │(SeaweedFS/MinIO)│   │
└────────────────┘ └─────────────────┘   │
         │                               │
         ▼                               ▼
     ┌───────────┐               ┌──────────────┐
     │   Trino   │               │    Airflow   │
     └───────────┘               └──────────────┘

```

## Source Code
How it works:
```
[You @ Jupyter Notebook in spark-iceberg:8888]
        │
        ▼
spark.writeTo("demo.nyc.taxis")
        │
        ▼
[REST Catalog @ iceberg-rest:8181]
  → registered warehouse = s3://warehouse/
        │
        ▼
[S3-compatible Storage @ MinIO:9000]
  /data/warehouse/demo/nyc/taxis/
      ├── data/
      └── metadata/
```

## Reference
https://iceberg.apache.org/spark-quickstart/
