study DGL dataloader


# How to scale up the graph using GraphDB? 

- [ ] 1. Store the whole graph into GraphDB
- [ ] 2. Divide train_nids into multiple non-overlapping sub-train_nids
- [ ] 3. Extract small-subgraphs which contain only the necessary parts for each sub-train_nids in (2)
- [ ] 4. Merge multiple train_dataloader as a large-train_dataloader, each link to a small-subgraph in (3)
- [ ] 5. Make sure the extract and build dataloader step (3) only occur when the corresponding sub-train_nids 
            is focused on.


