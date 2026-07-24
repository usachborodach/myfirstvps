local_backup_path="/home/user/backups/2026-07-23_wekan.zip"
remote_backup_zip="/root/backups/2026-07-23_wekan.zip"

scp "$local_backup_path" myfirstvps:/root/backups/
ssh myfirstvps "docker stop wekan"
ssh myfirstvps "unzip -o $remote_backup_zip -d /root/backups/"
ssh myfirstvps "docker exec -i mongo sh -c 'mongorestore --archive' < /root/backups/wekan.dump"
ssh myfirstvps "docker start wekan"