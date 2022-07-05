"""
- [X] Check the execution flow of add_graph_from_neo4j in https://github.com/jeffrey82221/ipycytoscape/blob/master/ipycytoscape/cytoscape.py
    - Step 1: get_node_labels_by_priority
    - Step 2: convert Neo4j nodes to cytoscape nodes
    - Step 3: convert Neo4j relationships to cytoscape edges
- [X] Map the execution flow to that of redisgraph
    - [X] Create Graph in Neo4j & RedisGraph 
    - [X] Using print to understand the flow 
    - [X] Copy the steps 1-3 for neo4j here 
    - [X] Try to find out the redisgraph version for each step 
- [ ] Extending RedisGraph to support Subgraph convertion:
    - [ ] Implement Unionable Graph objects
        REF: https://github.com/py2neo-org/py2neo/blob/master/py2neo/data.py
        - [ ] Subgrah: 
            __init__(self, nodes, relationships)
            __eq__ + __or__ + __str__
            nodes, edges
            nodes_count, edge_count
            add_node, add_edge
            labels、types
            (optional) __iter__、__bool__、__and__、__sub__、__xor__
        - [ ] Allow Path, Node, Edge to support union operation
            - [ ] Edge:
                add __or__ (a | b -> Subgraph) 
            - [ ] Node 
                add __or__ (a | b -> Subgraph) 
            - [ ] Path
                add __or__ (a | b -> Subgraph)
    - [ ] Implement the to_subgraph method:
        REF: https://github.com/py2neo-org/py2neo/blob/master/py2neo/cypher/__init__.py
        - [ ] add to_subgraph method to Edge, Node, & Path
        - [ ] add to_subgraph method to redisgraph.query_result.QueryResult
            - How: iterate over result_set of QueryResult
- [ ] Extending ipycytoscape's ipycytoscape/cytoscape.py
    - [ ] Add a customized to_subgraph method for converting result_set of RedisGraph
    - [ ] Build add_graph_from_redisgraph method following the NOTE(s) here
    - [ ] Once RedisGraph PR is done, substitude the `to_subgraph` to that of redisgraph version
"""
import json
from py2neo import Graph
from ipycytoscape import Node, Edge

"""
NOTE: 
_set_attributes & add_graph_from_neo4j are from ipycytoscape/cytoscape.py
"""
def _set_attributes(instance, data):
    cyto_attrs = instance._cyto_attrs + instance._base_cyto_attrs
    for k, v in data.items():
        if k in cyto_attrs:
            setattr(instance, k, v)
        else:
            instance.data[k] = v

def add_graph_from_neo4j(widget_graph, g):
    """
    Converts a py2neo Neo4j subgraph into a Cytoscape graph. It also adds
    a 'tooltip' node attribute to the Cytoscape graph if it is not present
    in the Neo4j subgraph. This attribute can be set as a tooltip by
    set_tooltip_source('tooltip'). The tooltip then displays the node
    properties from the Neo4j nodes.
    Parameters
    ----------
    g : py2neo Neo4j subgraph object
        See https://py2neo.org/v4/data.html#subgraph-objects
    """

    def convert_types_to_string(node_attributes):
        """
        Converts types not compatible with cytoscape to strings.
        Parameters
        ----------
        node_attributes : dictionary of node attributes
        """
        for k, v in node_attributes.items():
            try:
                json.dumps(v)
            except TypeError:
                node_attributes[k] = str(v)

        return node_attributes

    def get_node_labels_by_priority(g):
        """
        Returns a list of Neo4j node labels in priority order.
        If a Neo4j node has multiple labels, the most distinctive
        (least frequently occuring) label will appear first in this list.
        Example: five nodes have the labels (Person|Actor) and five nodes
        have the labels (Person|Director). In this case the Actor and Director
        labels have priority over the Person label.
        Parameters
        ----------
        g : py2neo Neo4j subgraph object
            See https://py2neo.org/v4/data.html#subgraph-objects
        """
        counts = dict()

        # This counts the number of instances that a node has a particular
        # label (a node can have multiple labels in Neo4j).
        # counts.get(label, 0) initializes the count with zero, and then
        # increments the value if more of the same labels are encountered.
        for node in g.nodes:
            for label in node.labels:
                counts[label] = counts.get(label, 0) + 1

        return sorted(counts, key=counts.get)

    def create_tooltip(node_attributes, node_labels):
        """
        Returns a string of node labels and node attributes to be used as a tooltip.
        Parameters
        ----------
        node_attributes : dictionary of node attributes
        node_labels : list of node labels
        """
        labels = ",".join(label for label in node_labels)
        attributes = "\n".join(k + ":" + str(v) for k, v in node_attributes.items())
        return labels + "\n" + attributes

    # select labels to be displayed as node labels
    priority_labels = get_node_labels_by_priority(g)

    # convert Neo4j nodes to cytoscape nodes
    node_list = list()
    for node in g.nodes:
        node_attributes = dict(node)
        # NOTE: # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Explain dict(node):
        # Node('Country', 'Location', areaSqKm=1972550, id='MX', iso='MX', iso3='MEX', isoNumeric='484', name='Mexico')
        #  -> {'isoNumeric': '484', 'iso': 'MX', 'name': 'Mexico', 'id': 'MX', 'areaSqKm': 1972550, 'iso3': 'MEX'}
        # RedisGraph: 
        # 1. g.nodes -> get_nodes_and_edges(result)[0]
        # 2. dict(node) -> node.properties
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

        # convert Neo4j specific types to string
        node_attributes = convert_types_to_string(node_attributes)

        # create tooltip text string
        if "tooltip" not in node_attributes:
            tooltip_text = create_tooltip(node_attributes, node.labels)
            node_attributes["tooltip"] = tooltip_text

        # assign unique id to node
        node_attributes["id"] = node.identity
        # NOTE: # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # Explain node.identity -> 301416 (int)
        # RedisGraph: 
        # node.identity -> node.id
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

        # assign class label with the highest priority
        index = len(priority_labels)
        for label in node.labels:
            # NOTE: # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
            # Explain node.labels 
            # Node('Country', 'Location', areaSqKm=1972550, id='MX', iso='MX', iso3='MEX', isoNumeric='484', name='Mexico')
            # -> ['Location', 'Country']
            # RedisGraph: 
            # 1. g.nodes -> get_nodes_and_edges(result)[0]
            # 2. node.labels -> node.labels
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
            index = min(index, priority_labels.index(label))

        node_attributes["label"] = priority_labels[index]

        # create node
        node_instance = Node()
        _set_attributes(node_instance, node_attributes)
        node_list.append(node_instance)

    widget_graph.add_nodes(node_list)

    # convert Neo4j relationships to cytoscape edges
    edge_list = list()
    for rel in g.relationships:
        edge_instance = Edge()

        # create dictionaries of relationship
        rel_attributes = dict(rel)
        # NOTE: # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # Explain dict(rel): 
        # rel: IN(Node('City', 'Location', geonameId='11085890', id='11085890', location=(-99.64723, 18.94931), name='San Francisco', population=3165), 
        #        Node('Admin2', 'Location', geonameId='8583691', id='MX.15.113', location=(-99.67353, 18.96396), name='Villa Guerrero', parentId='MX.15'))
        # -> {}
        # RedisGraph: 
        # 1. g.relationships -> get_nodes_and_edges(result)[1]
        # 2. dict(rel) -> rel.properties
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

        # convert Neo4j specific types to string
        rel_attributes = convert_types_to_string(rel_attributes)

        # assign name of the relationship
        if "name" not in rel_attributes:
            rel_attributes["name"] = rel.__class__.__name__
        # NOTE: # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # Explain rel.__class__.__name__ 
        # Type of the relationship 
        # IN(Node('City', 'Location', geonameId='3519337', id='3519337', location=(-98.00209, 20.55254), name='San Francisco', population=3353), 
        #    Node('Admin2', 'Location', geonameId='8583728', id='MX.30.083', location=(-98.01656, 20.72862), name='Ixhuatlan de Madero', parentId='MX.30'))
        # -> "IN"
        # RedisGraph: 
        # 1. rel.__class__.__name__ -> rel.relation
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

        # assign unique node ids
        edge_instance.data["source"] = rel.start_node.identity
        edge_instance.data["target"] = rel.end_node.identity
        # NOTE: # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Explain rel.start_node , rel.end_node : get the start and end nodes of the relationship
        # start_node: City 
        # end_node: Admin2
        # RedisGraph: 
        # 1. rel.start_node.identity -> rel.src_node
        # 2. rel.end_node.identity -> rel.dest_node
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        _set_attributes(edge_instance, rel_attributes)

        edge_list.append(edge_instance)

    # Neo4j graphs are directed and may have multiple edges
    directed = True
    multiple_edges = True

    widget_graph.add_edges(edge_list, directed, multiple_edges)


import ipycytoscape
widget1 = ipycytoscape.CytoscapeWidget()
widget_graph = widget1.graph
print('Graph widget CREATED')
from py2neo import Graph
graph = Graph("bolt://132.249.238.185:7687", user="reader", password="demo")
query1 = """
MATCH p=(:City{name:'San Francisco'})-[:IN*]->(:World) RETURN p
"""

subgraph = next(graph.run(query1)).to_subgraph() # This is a py2neo.data.Path object
# subgraph = graph.run(query1).to_subgraph() # Execute this produce a subgraph which is the union of all py2neo.data objects (e.g., Path, Node, Edges)
print('Get Subgraph')
print('Create widget')
add_graph_from_neo4j(widget_graph, subgraph)
print('SUCCESFULLY add Graph into Widget')

"""
NOTE:
meaning of multiple edges: there can be more than one edges between two nodes
"""