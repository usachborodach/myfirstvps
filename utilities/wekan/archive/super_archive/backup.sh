#!/bin/bash
docker stop gorbov_wekan
docker exec gorbov_mongo sh -c 'mongodump --archive' > /home/user/dumps/$(date -I).dump
docker start gorbov_wekan
curl -X POST "http://192.168.81.222:5657/upload/share" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F file=@/home/user/dumps/$(date -I).dump
find /home/user/dumps/ -type f -print -mtime +30 -delete