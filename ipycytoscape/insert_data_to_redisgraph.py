import redis
from redisgraph import Node, Edge, Graph, Path

def get_nodes_and_edges(result):
    nodes = dict()
    edges = dict()
    for record in result.result_set:
        for element in record:
            if isinstance(element, Node):
                if element.id not in nodes:
                    nodes[element.id] = element
            elif isinstance(element, Edge):
                if element.id not in edges:
                    edges[element.id] = element
            elif isinstance(element, Path):
                for node in element.nodes():
                    if node.id not in nodes:
                        nodes[node.id] = node
                for edge in element.edges():
                    if edge.id not in edges:
                        edges[edge.id] = edge
    nodes = list(nodes.values())
    edges = list(edges.values())
    return nodes, edges



r = redis.Redis(host='localhost', port=6379)

redis_graph = Graph('social', r)

john = Node(label='person', properties={'name': 'John Doe', 'age': 33, 'gender': 'male', 'status': 'single'})
redis_graph.add_node(john)

japan = Node(label='country', properties={'name': 'Japan'})
redis_graph.add_node(japan)

edge = Edge(john, 'visited', japan, properties={'purpose': 'pleasure'})
redis_graph.add_edge(edge)

jeffrey = Node(label='person', properties={'name': 'Jeffrey', 'age': 33, 'gender': 'male', 'status': 'single'})
redis_graph.add_node(jeffrey)

china = Node(label='country', properties={'name': 'China'})
redis_graph.add_node(china)

edge = Edge(jeffrey, 'visited', china, properties={'purpose': 'work'})
redis_graph.add_edge(edge)

edge = Edge(john, 'visited', china, properties={'purpose': 'work'})
redis_graph.add_edge(edge)

edge = Edge(jeffrey, 'visited', japan, properties={'purpose': 'pleasure'})
redis_graph.add_edge(edge)

edge = Edge(china, 'left_to', japan)
redis_graph.add_edge(edge)

edge = Edge(japan, 'right_to', china)
redis_graph.add_edge(edge)

redis_graph.commit()

"""
Phase I: Check elements in result
"""

query = """MATCH p=()-[v]->() -[]-> ()
           RETURN p"""
result = redis_graph.query(query)


# Print resultset
result.pretty_print()

print(result.result_set)

print(result.result_set[0][0])

print(result.result_set[2][0])

japan_node_1 = [n for n in result.result_set[0][0].nodes()][1]
japan_node_2 = [n for n in result.result_set[2][0].nodes()][0]
print(japan_node_1, japan_node_1.id, japan_node_1.labels, japan_node_1.properties)
print(japan_node_2, japan_node_2.id, japan_node_2.labels, japan_node_2.properties)
assert japan_node_1 == japan_node_2
right_to_edge_1 = [n for n in result.result_set[0][0].edges()][1]
right_to_edge_2 = [n for n in result.result_set[2][0].edges()][0]
assert right_to_edge_1 == right_to_edge_2
print(right_to_edge_1, right_to_edge_1.id, right_to_edge_1.relation, right_to_edge_1.properties, right_to_edge_1.src_node, right_to_edge_1.dest_node)
print(right_to_edge_2, right_to_edge_2.id, right_to_edge_2.relation, right_to_edge_1.properties, right_to_edge_2.src_node, right_to_edge_2.dest_node)

# Convert Paths, Nodes, Edges Data of RedisGraph into Simply Nodes and Edges
"""
Phase II: Organize result elements into unique nodes and unique paths
"""
from redisgraph import Node, Edge, Graph, Path

query = """MATCH p=()-[v]->() -[]-> ()
           RETURN p"""
# TODO:
# add to_subgraph functionality to redisgraph redisgraph.query_result.QueryResult object
# similar to py2neo: graph.run(query1).to_subgraph()
result = redis_graph.query(query)
print('Result:')
print(result)
print([record for record in result.result_set][0])
# NOTE: 
# record in redisgraph is basically a list of elements
nodes, edges = get_nodes_and_edges(result)
print('Nodes:')
print(nodes[0:2])
print('Edges:')
print(edges[0:2])