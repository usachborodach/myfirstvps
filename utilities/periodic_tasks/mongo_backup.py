import os
import subprocess
import zipfile
from datetime import date

MAX_BACKUPS = 30
BACKUPS_DIR = '/root/backups'

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
    zip_file_path = f'{BACKUPS_DIR}/{date.today()}_mongo.zip'
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write('mongo.dump', os.path.basename('mongo.dump'))
    os.remove('mongo.dump')
    files = [f for f in os.listdir(BACKUPS_DIR) if f.endswith('.zip')]
    files.sort()
    if len(files) > MAX_BACKUPS:
        to_delete = len(files) - MAX_BACKUPS
        for f in files[:to_delete]:
            file_path = os.path.join(BACKUPS_DIR, f)
            try:
                os.remove(file_path)
                print(f"Удалён старый архив: {file_path}")
            except Exception as e:
                print(f"Не удалось удалить {file_path}: {e}")

if __name__ == "__main__":
    main()