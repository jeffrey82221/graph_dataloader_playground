from official.full_graph import prepare_full_graph
import dgl
import networkx as nx
graph = prepare_full_graph()



# Save Node Features & Edge Features into DB (here H5 file is used)
# - For heterogeneous graph use different table for different features and different edges

# Save Node Ids & Edge Ids into Redis Graph using Cypher 