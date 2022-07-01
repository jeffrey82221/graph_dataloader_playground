# Installation of Python3.8
apt-get install software-properties-common
add-apt-repository -y ppa:deadsnakes/ppa
apt update
apt install python3.8
apt install python3.8-venv
# Start Virtual Environment of Python3.8 
python3.8 -m venv env
source env/bin/activate
# Install pycograph 
pip install pycograph
# Start or Restart RedisGraph 
/usr/local/lib/python3.6/site-packages/redis_server/bin/redis-server --port 6379 --loadmodule /usr/local/lib/redisgraph/redisgraph.so
