docker run -d \
  --restart=always \
  --name mongo \
  --network wekan-net \
  -p 127.0.0.1:27017:27017 \
  mongo