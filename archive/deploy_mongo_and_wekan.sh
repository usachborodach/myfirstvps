docker network create wekan-net

docker run -d \
  --restart=always \
  --name mongo \
  --network wekan-net \
  -p 127.0.0.1:27017:27017 \
  mongo

docker run -d \
  --restart=always \
  --name wekan \
  --network wekan-net \
  -e "WITH_API=true" \
  -e "MONGO_URL=mongodb://mongo:27017/wekan" \
  -e "ROOT_URL=http://84.54.57.22:2000" \
  -p 2000:8080 \
  wekanteam/wekan:v6.22