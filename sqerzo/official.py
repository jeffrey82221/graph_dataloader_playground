from dataclasses import dataclass

from sqerzo import GraphEdge, GraphNode, SQErzoGraph

@dataclass
class MeetEdge(GraphEdge):
    pass
    
@dataclass
class UserNode(GraphNode):
    name: str = None

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
            u1 = UserNode(name=f"UName-{n}")
            d1 = UserNode(name=f"DName-{n}")

            tx.add(u1)
            tx.add(d1)

            u1_meet_g1 = MeetEdge(
                source=u1,
                destination=d1
            )
            tx.add(u1_meet_g1)


# conn_str = "neo4j://neo4j:esb1313@127.0.0.1:7687/?graph=email"
conn_str = "redis://127.0.0.1:6379/?graph=email"
create_graph(conn_str)
gh = SQErzoGraph(conn_str)
q = gh.Query.raw(
        "match (u1)-[:Meet]->(u2) return u1, u2"
    ).execute(map_to={"u1": UserNode, "u2": UserNode})
print('Node Tuples:', q)
q = gh.Query.raw(
        "match (u:User) return u"
    ).execute()
print('Nodes:', q)
q = gh.Query.raw(
        "match ()-[e]-() return e"
    ).execute()
print('Edges:', q)
# TODO: 
# FIX: 
# 1. [ ] Edge seems to not saved in both neo4j & redisgraph version
# TEST:
# 1. [ ] Make sure q return from both redisgraph & neo4j are the same 