import redis
import sys
import time
import yaml
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

class RedisExporter(object):
    def __init__(self, query, r):
        self.query = query
        self.redis = r

    def collect(self):
        for metric_name in self.query['metrics']:
            metric = self.query['metrics'][metric_name]

            yield GaugeMetricFamily(
                metric.get('name', metric_name),
                metric['description'],
                value = float(self.redis.execute_command(metric['query']))
            )

if __name__ == "__main__":
    if len(sys.argv) == 0:
        raise "The path of the query file is needed"

    with open(sys.argv[1], 'r') as yaml_query:
        try:
            query = yaml.load(yaml_query)['prometheus_redis']
        except yaml.YAMLError as e:
            print(e)

    conn = query['connection']
    r = redis.Redis(
        host = conn.get('host', 'localhost'),
        port = conn.get('port', 6379),
        db = conn.get('database', 0),
        password = conn.get('password', None)
    )

    REGISTRY.register(RedisExporter(query, r))
    start_http_server(9118)
    while True: time.sleep(1)
