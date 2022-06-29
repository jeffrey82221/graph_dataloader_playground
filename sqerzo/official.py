from dataclasses import dataclass

from sqerzo import GraphEdge, GraphNode, SQErzoGraph

class MeetEdge(GraphEdge):
    pass

@dataclass
class UserNode(GraphNode):
    name: str = None

    
def create_graph(connection_string: str):
    gh = SQErzoGraph(connection_string)
    gh.truncate()  # Drop database
    
    u1 = UserNode(name=f"UName-1")
    gh.save(u1)
    
    d1 = UserNode(name=f"DName-2")
    gh.save(d1)
        
    u1_meet_g1 = MeetEdge(
        source=u1,
        destination=d1
    )
    gh.save(u1_meet_g1)
        


# create_graph("redis://127.0.0.1:6379/?graph=email")
# conn_str = "neo4j://neo4j:esb1313@127.0.0.1:7687/?graph=email"
conn_str = "redis://127.0.0.1:6379/?graph=email"
create_graph(conn_str)
gh = SQErzoGraph(conn_str)
q = gh.Query.raw(
        "match (u1:User)-[:Meet]->(u2:User) return u1, u2"
    ).execute(map_to={"u1": UserNode, "u2": UserNode})
print(q)
# TODO: 
# FIX: Edge seems to not saved in both neo4j & redisgraph version