# Install Redis Stack (includes Redis 7.0.0 / RedisInsight / RedisGraph 2.8.12)
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
apt-get update
apt-get install redis-stack-server
# Install redis-server 6.0.9
pip install redis-server
# Install RedisInsight from source 
# https://github.com/RedisInsight/RedisInsight/wiki/How-to-build-and-contribute
# 1. Install yarn and nodes
apt update
apt install -y curl
curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
apt update
apt install -y yarn
curl -sL https://deb.nodesource.com/setup_15.x | bash -
apt install -y nodejs
# 2. Install webpack
npm intall webpack
npm install webpack-dev-server -g
# 2. Before development or build you have to install required dependencies
yarn install
yarn add -D webpack-cli
yarn --cwd redisinsight/api/
