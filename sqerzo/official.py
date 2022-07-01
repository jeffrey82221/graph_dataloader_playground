from dataclasses import dataclass

from sqerzo import GraphEdge, GraphNode, SQErzoGraph

@dataclass
class MeetEdge(GraphEdge):
    pass

@dataclass
class DriveEdge(GraphEdge):
    pass

@dataclass
class UserNode(GraphNode):
    name: str = None
    sex: bool = None

@dataclass
class CarNode(GraphNode):
    color: str = None
"""
TODO: FIX: Currently saving of edge has bug
def create_graph(connection_string: str):
    gh = SQErzoGraph(connection_string)
    gh.truncate()  # Drop database
    
u1 = UserNode(name=f"UName-1")

d1 = UserNode(name=f"DName-2")
    
u1_meet_g1 = MeetEdge(
    source=u1,
    destination=d1
)
    gh.save(u1_meet_g1)
"""

def create_graph(connection_string: str):
    gh = SQErzoGraph(connection_string)
    gh.truncate()  # Drop database

    with gh.transaction() as tx:  # Transaction starts here

        for n in range(1):  # Inserts 1000 nodes (500 * 2) and 500 relations
            u1 = UserNode(name=f"UName-{n}", sex=0)
            d1 = UserNode(name=f"DName-{n}", sex=1)

            tx.add(u1)
            tx.add(d1)

            u1_meet_g1 = MeetEdge(
                source=u1,
                destination=d1
            )
            tx.add(u1_meet_g1)

            c1 = CarNode(color='red')
            tx.add(c1)

            u1_drive_c1 = DriveEdge(
                source=u1,
                destination=c1
            )
            tx.add(u1_drive_c1)

def extract_examples(conn_str):
    create_graph(conn_str)
    gh = SQErzoGraph(conn_str)
    node_tuples_q = gh.Query.raw(
            "match (u1)-[:Meet]->(u2) return u1, u2"
        ).execute(map_to={"u1": UserNode, "u2": UserNode})
    # print('Node Tuples:', node_tuples_q)
    nodes_q = gh.Query.raw(
            "match (u:User) return u"
        ).execute()
    car_nodes_q = gh.Query.raw(
            "match (c:Car) return c"
        ).execute()
    # print('Nodes:', nodes_q)
    edges_q = gh.Query.raw(
            "match ()-[e]-() return e"
        ).execute()
    drive_edges_q = gh.Query.raw(
            "match ()-[e:Drive]-() return e"
        ).execute()
    return node_tuples_q, nodes_q, edges_q, drive_edges_q, car_nodes_q


# conn_str = "redis://127.0.0.1:6379/?graph=email"

# TODO: 
# FIX: 
# 1. [X] Allow Edge to be saved and retrieved for both neo4j & redisgraph 
# 2. [ ] Avoid Repeat Extraction of Edges
# 3. [ ] Allow Extracted Edge to Show Nodes in properties
# TEST:
# 2. [X] Make sure q return from both redisgraph & neo4j are the same 

neo_node_tuples_q, neo_nodes_q, neo_edges_q, neo_drive_edges_q, neo_car_nodes_q = extract_examples("neo4j://neo4j:esb1313@127.0.0.1:7687/?graph=email")
redis_node_tuples_q, redis_nodes_q, redis_edges_q, redis_drive_edges_q, redis_car_nodes_q = extract_examples("redis://127.0.0.1:6379/?graph=email")
import pprint
print('Node Tuples:')
pprint.pprint(neo_node_tuples_q)
pprint.pprint(redis_node_tuples_q)
print()
print('Nodes:')
pprint.pprint(neo_nodes_q)
pprint.pprint(redis_nodes_q)
print()
print('Edges:')
print('neo:')
pprint.pprint(neo_edges_q)
print('redis:')
pprint.pprint(redis_edges_q)
print()
print('Drive Edges:')
print('neo:')
pprint.pprint(neo_drive_edges_q)
print('redis:')
pprint.pprint(redis_drive_edges_q)
print()
print('Car Nodes:')
pprint.pprint(neo_car_nodes_q)
pprint.pprint(redis_car_nodes_q)
print()

