import sys
import os
base_path = os.path.dirname(__file__)

mongo_backup_path = f'{base_path}/../mongo_backup'
sys.path.append(mongo_backup_path)
from mongo_backup import mongo_backup

def main():
    mongo_backup()

if __name__ == "__main__":
    main()