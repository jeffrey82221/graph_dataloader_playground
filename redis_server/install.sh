apt install redis-server
cd /content/
apt-get install build-essential cmake m4 automake peg libtool autoconf
git clone --recurse-submodules -j8 https://github.com/RedisGraph/RedisGraph.git
cd RedisGraph
make
pip install -r tests/requirements.txt
cp -r src /usr/local/lib/redisgraph
cd ..
rm -rf RedisGraph