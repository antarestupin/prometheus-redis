# Prometheus Redis

A service that exposes Prometheus metrics for Redis command results.

## Install

```
git clone https://github.com/antarestupin/prometheus-redis.git && cd prometheus-redis
pip install -r requirements.txt
```

## Usage

```
python exporter.py /path/to/queries.yml
```

An example of queries file is provided in example_queries.yml
