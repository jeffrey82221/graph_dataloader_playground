# Install Pytorch for CUDA 11.3
# -> torch==1.11.0+cu113
# -> torchvision==0.12.0+cu113
# -> torchaudio==0.11.0+cu113
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
# Install Pytorch-Geometric for CUDA 11.3 and pytorch 1.11.*
# -> torch_scatter==2.0.9
# -> torch_sparse==0.6.14
# -> torch_cluster==1.6.0
# -> torch_spline_conv==1.2.1
# -> torch_geometric==2.0.4
pip install torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric -f https://data.pyg.org/whl/torch-1.11.0+cu113.html