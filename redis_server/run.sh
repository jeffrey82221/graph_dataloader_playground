# Run Redis-Stack-Server (with RedisGraph inside)
redis-stack-server
# Running RedisInsight from Source
git clone https://github.com/RedisInsight/RedisInsight.git
cd RedisInsight
# 1. Run BackEnd
yarn --cwd redisinsight/api/ start:dev
# 2. Run FrontEnd
yarn start:web