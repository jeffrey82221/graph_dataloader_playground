# https://docs.dgl.ai/tutorials/large/L1_large_node_classification.html
import dgl
import torch
import numpy as np
from ogb.nodeproppred import DglNodePropPredDataset

# Loading Dataset
dataset = DglNodePropPredDataset('ogbn-arxiv')
device = 'cpu'      # change to 'cuda' for GPU

# Preprocess the Graph
graph, node_labels = dataset[0]
# Add reverse edges since ogbn-arxiv is unidirectional.
graph = dgl.add_reverse_edges(graph)
graph.ndata['label'] = node_labels[:, 0]
print(graph)
print(node_labels)

node_features = graph.ndata['feat']
num_features = node_features.shape[1]
num_classes = (node_labels.max() + 1).item()
print('Number of features:', num_features)
print('Number of classes:', num_classes)

# Get Splitting Nodes:
idx_split = dataset.get_idx_split()
train_nids = idx_split['train']
valid_nids = idx_split['valid']
test_nids = idx_split['test']

# Defining Neighbor Sampler and Data Loader in DGL
# To write your own neighbor sampler, please refer to this user guide section.
# https://docs.dgl.ai/guide/minibatch-custom-sampler.html#guide-minibatch-customizing-neighborhood-sampler


sampler = dgl.dataloading.NeighborSampler([4, 4])
train_dataloader = dgl.dataloading.DataLoader(
    # The following arguments are specific to DGL's DataLoader.
    graph,              # The graph
    train_nids,         # The node IDs to iterate over in minibatches
    sampler,            # The neighbor sampler
    device=device,      # Put the sampled MFGs on CPU or GPU
    # The following arguments are inherited from PyTorch DataLoader.
    batch_size=4,    # Batch size
    shuffle=True,       # Whether to shuffle the nodes for every epoch
    drop_last=False,    # Whether to drop the last incomplete batch
    num_workers=0       # Number of sampler processes
)
valid_dataloader = dgl.dataloading.DataLoader(
    graph, valid_nids, sampler,
    batch_size=1024,
    shuffle=False,
    drop_last=False,
    num_workers=0,
    device=device
)
if __name__ == '__main__':
    # Check the Output of Dataloader Yieldings
    input_nodes, output_nodes, mfgs = example_minibatch = next(iter(train_dataloader))
    print(example_minibatch)
    print("To compute {} nodes' outputs, we need {} nodes' input features".format(len(output_nodes), len(input_nodes)))
    print("MGDS: {}".format(str(mfgs)))

    mfg_0_src = mfgs[0].srcdata[dgl.NID]
    mfg_0_dst = mfgs[0].dstdata[dgl.NID]
    print(mfg_0_src)
    print(mfg_0_dst)
    # src nodes in the beginning are the dst nodes:
    print(torch.equal(mfg_0_src[:mfgs[0].num_dst_nodes()], mfg_0_dst))