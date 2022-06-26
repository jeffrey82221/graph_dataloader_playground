from ogb.nodeproppred import DglNodePropPredDataset
import dgl
def prepare_full_graph():
    dataset = DglNodePropPredDataset('ogbn-arxiv')
    # Preprocess the Graph
    graph, node_labels = dataset[0]
    # Add reverse edges since ogbn-arxiv is unidirectional.
    graph = dgl.add_reverse_edges(graph)
    graph.ndata['label'] = node_labels[:, 0]
    print(graph)
    return graph

def get_splits():
    dataset = DglNodePropPredDataset('ogbn-arxiv')
    # Get Splitting Nodes:
    idx_split = dataset.get_idx_split()
    train_nids = idx_split['train']
    valid_nids = idx_split['valid']
    test_nids = idx_split['test']
    return train_nids, valid_nids, test_nids