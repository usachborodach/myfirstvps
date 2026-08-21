#Deploy
docker run -d --restart=always --name gorbov_mongo -p 27017:27017 mongo
docker run -d --restart=always --name gorbov_wekan --link "gorbov_mongo:db" -e "WITH_API=true" -e "MONGO_URL=mongodb://gorbov_mongo:27017/wekan" -e "ROOT_URL=http://192.168.1.200:2000" -p 2000:8080 wekanteam/wekan:v6.22
docker run -d --restart=always --name gorbov_mongo_express --link "gorbov_mongo:db" -e "ME_CONFIG_MONGODB_URL=mongodb://gorbov_mongo:27017/" -p 8081:8081 mongo-express

#Backup
#!/bin/bash
docker stop gorbov_wekan
docker exec gorbov_mongo sh -c 'mongodump --archive' > /home/user/Downloads/$(date -I).dump
docker start gorbov_wekan
curl -X POST "http://192.168.81.222:5657/upload/share" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F file=@/home/user/dumps/$(date -I).dump
find /home/user/dumps/ -type f -print -mtime +30 -delete

#cron
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
0 6 * * * /home/user/repos/ShuraRepo/organizer/wekan/archive/backup.sh

#Restore 
docker stop gorbov_wekan
docker exec -i gorbov_mongo sh -c 'mongorestore --archive' < /home/user/dumps/2025-07-12.dump
docker start gorbov_wekan

#Archive
docker stop gorbov_wekan
docker exec gorbov_mongo rm -rf /data/dump
docker cp /home/user/gorbov/dumps/2025-01-12.dump gorbov_mongo:/data/dump.bson
docker exec gorbov_mongo mongorestore --drop --dir=/data/dump.bson
docker start gorbov_wekan



#========================== Вариант для Вахтанга
#Первый вариант (аватарки)
docker run -d --restart=always -p 27017:27017 --name wekan-db mongo:5
docker run -d --restart=always --name wekan --link "wekan-db:db" -e "WITH_API=true" -e "MONGO_URL=mongodb://wekan-db:27017/wekan" -e "ROOT_URL=http://192.168.1.200:2000" -p 2000:8080 wekanteam/wekan:v5.41

# исправленный дамп
#!/bin/bash
find /mnt/fileshare/WekanDumps/ -type f -print -mtime +30 -delete
cd /mnt/fileshare/WekanDumps/
docker stop wekan
docker exec wekan-db sh -c 'mongodump --archive' > /mnt/fileshare/WekanDumps/$(date -I).dump
docker start wekan

#Дамп-рестор (старый)
docker exec wekan-db sh -c 'mongodump --archive' > /mnt/fileshare/WekanDumps/$(date -I).dump

docker exec wekan-db sh -c 'mongodump --archive' > /mnt/fileshare/WekanDumps/$(date -I).dump
docker exec -i wekan-db sh -c 'mongorestore --archive' < /mnt/fileshare/WekanDumps/2024-09-09.dump

docker exec wekan-db sh -c 'mongodump --archive' > /mnt/fileshare/WekanDumps/test.dump

#Убрать хлам за докером
docker container prune -f
docker image prune -f
docker volume prune -f