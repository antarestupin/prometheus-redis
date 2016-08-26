import redis
import sys
import time
import yaml
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

class RedisExporter(object):
    def __init__(self, query, redisConnections):
        self.query = query
        self.redisConnections = redisConnections

    def collect(self):
        for metric_name in self.query['metrics']:
            metric = self.query['metrics'][metric_name]
            value = self.redisConnections[metric['connection']].execute_command(metric['query'])

            yield GaugeMetricFamily(
                metric.get('name', metric_name),
                metric['description'],
                value = float(value)
            )

if __name__ == "__main__":
    if len(sys.argv) == 0:
        raise "The path of the query file is needed"

    with open(sys.argv[1], 'r') as yaml_query:
        try:
            query = yaml.load(yaml_query)['prometheus_redis']
        except yaml.YAMLError as e:
            print(e)

    redisConnections = {}
    for conn in query['connections']:
        connParams = query['connections'][conn]
        redisConnections[conn] = redis.Redis(
            host = connParams.get('host', 'localhost'),
            port = connParams.get('port', 6379),
            db = connParams.get('database', 0),
            password = connParams.get('password', None)
        )

    REGISTRY.register(RedisExporter(query, redisConnections))
    start_http_server(query.get('server', {}).get('port', 9118))
    while True: time.sleep(1)
