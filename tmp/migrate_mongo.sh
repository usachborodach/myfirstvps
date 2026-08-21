#!/bin/bash
backup_date="2026-08-21"
ordinary_zip_path="/home/user/backups/"$backup_date"_wekan.zip"
tmp_zip_path="/tmp/"$backup_date"_wekan.zip"

ssh myfirstvps "python3 /root/myfirstvps/tmp/export_some_data.sh"

ssh work "/usr/bin/python3 /home/user/repos/ShuraRepo/organizer/reminder/backup.py"
scp work:"$ordinary_zip_path" "$tmp_zip_path"
scp "$tmp_zip_path" myfirstvps:$tmp_zip_path

ssh myfirstvps "docker stop wekan"
ssh myfirstvps "docker rm -f mongo"
ssh myfirstvps "docker run -d --restart=always --name mongo --network wekan-net -p 127.0.0.1:27017:27017 mongo"
ssh myfirstvps "unzip -o $tmp_zip_path -d /tmp/"
ssh myfirstvps "docker exec -i mongo sh -c 'mongorestore --archive' < /tmp/wekan.dump"
ssh myfirstvps "docker start wekan"

ssh myfirstvps "python3 /root/myfirstvps/tmp/import_some_data.py"
ssh myfirstvps "python3 /root/myfirstvps/tmp/create_indexes.py"