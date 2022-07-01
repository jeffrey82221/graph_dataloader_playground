# Extract Code Graph into RedisGraph 
cd <the directory of interest>
pycograph load --project-dir .
# Test content in RedisGraph using its python package
```python
import redis
from redisgraph import Graph
r = redis.Redis(host='localhost', port=6379)
redis_graph = Graph('.', r) 
# "." can be replace by the folder name of the codebase
redis_graph.query('MATCH (n) RETURN n').pretty_print()
```