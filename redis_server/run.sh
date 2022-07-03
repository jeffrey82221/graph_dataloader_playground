# Run Redis-Stack-Server (with RedisGraph inside) - port: 6379
redis-stack-server
# Running RedisInsight from Source
git clone https://github.com/RedisInsight/RedisInsight.git
cd RedisInsight
yarn --cwd redisinsight/api/
# 1. Run BackEnd - port: 5000
yarn --cwd redisinsight/api/ start:dev
# 2. Run FrontEnd - port: 8080
yarn add -D webpack-cli
yarn --yes start:web
