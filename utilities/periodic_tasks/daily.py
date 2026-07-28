import sys
import os

base_path = os.path.dirname(__file__)
mongo_backup_path = f'{base_path}/../mongo_backup'

sys.path.append('/root/home/user/repos/myfirstvps/utilities/mongo_backup')
from mongo_backup import mongo_backup

def main():
    mongo_backup()

if __name__ == "__main__":
    main()