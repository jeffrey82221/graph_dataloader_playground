# Install Redis Stack (includes Redis 7.0.0 / RedisInsight / RedisGraph 2.8.12)
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
apt-get update
apt-get install redis-stack-server
# Install redis-server 6.0.9
pip install redis-server
# Install redisinsight (not working)
curl -O https://downloads.redisinsight.redislabs.com/latest/redisinsight-linux64
mkdir /usr/local/redisinsight
mv redisinsight-linux64-1.12.0 /usr/local/redisinsight/redisinsight-1.12.0
chmod +x /usr/local/redisinsight/redisinsight-1.12.0
nohup /usr/local/redisinsight/redisinsight-1.12.0
echo "export REDISINSIGHT_HOST=127.0.0.1" >> ~/.bash_profile
echo "export REDISINSIGHT_HOST_DIR=/usr/local/redisinsight/.redisinsight" >> ~/.bash_profile
source ~/.bash_profile