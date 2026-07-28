import os
import subprocess
import zipfile
from datetime import date

def main():
    mongo_backup()

def mongo_backup():
    command = ['docker', 'stop', 'wekan']
    subprocess.run(command)
    command = ['docker', 'exec', 'mongo', 'sh', '-c', 'mongodump --archive']
    mongo_dump = subprocess.run(command, capture_output=True, text=False)
    command = ['docker', 'start', 'wekan']
    subprocess.run(command)
    with open('mongo.dump', 'wb') as f:
        f.write(mongo_dump.stdout)
    zip_file_path = f'/root/backups/{date.today()}_mongo.zip'
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write('mongo.dump', os.path.basename('mongo.dump'))
    os.remove('mongo.dump')

if __name__ == "__main__":
    main()