import redis
from redis.commands.graph import Node, Edge, Graph, Path

r = redis.Redis(host='localhost', port=6379)

redis_graph = r.graph()



john = Node(label='person', properties={'name': 'John Doe', 'age': 33, 'gender': 'male', 'status': 'single'})
redis_graph.add_node(john)

japan = Node(label='country', properties={'name': 'Japan'})
redis_graph.add_node(japan)

edge = Edge(john, 'visited', japan, properties={'purpose': 'pleasure'})
redis_graph.add_edge(edge)

redis_graph.commit()


query = """MATCH (p:person)-[v:visited {purpose:"pleasure"}]->(c:country)
           RETURN p.name, p.age, v.purpose, c.name"""

result = redis_graph.query(query)


for record in result.result_set:
    print(record)