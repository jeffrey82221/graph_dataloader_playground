# Install RedisServer v4.0.9
apt install redis-server
# Install RedisGraph 2.8.15 from source
# NOTE: another way to update RedisGraph is to download the tagged released zip file
# and move it into Aicloud for build. 
cd /content/
apt-get install build-essential cmake m4 automake peg libtool autoconf
git clone --recurse-submodules -j8 https://github.com/RedisGraph/RedisGraph.git
cd RedisGraph
make
# pip install -r tests/requirements.txt
cp -r src /usr/local/lib/redisgraph
cd ..
rm -rf RedisGraph
# Install redis-server 6.0.9
pip install redis-server
# TODO: Install RedisInsight from source
