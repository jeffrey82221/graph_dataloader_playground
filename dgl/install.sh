# (Experimental) Downgrade CUDA from 11.1 to 11.0 to check if DGL and Pytorch cu11.3 work on CUDA 11.0 
# only do this on colab
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin
mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget http://developer.download.nvidia.com/compute/cuda/11.0.2/local_installers/cuda-repo-ubuntu1804-11-0-local_11.0.2-450.51.05-1_amd64.deb
dpkg -i cuda-repo-ubuntu1804-11-0-local_11.0.2-450.51.05-1_amd64.deb
apt-key add /var/cuda-repo-ubuntu1804-11-0-local/7fa2af80.pub
apt-get update
apt-get install cuda-11.0
# Install Pytorch for CUDA 11.3
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
# Install DGL for CUDA 11.3
pip install dgl-cu113 dglgo -f https://data.dgl.ai/wheels/repo.html