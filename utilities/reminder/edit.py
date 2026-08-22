import subprocess

SOURCE_PATH = '/root/myfirstvps/utilities/reminder/reminders.csv'
LOCAL_PATH = '/tmp/reminders.csv'

def main():
    download_csv()
    open_with_nano()

def download_csv():
    command = ['scp', f'myfirstvps:{SOURCE_PATH}', LOCAL_PATH]
    subprocess.run(command)

def open_with_nano():
    command = ['nano', LOCAL_PATH]
    subprocess.run(command)

def upload_csv():
    command = ['scp', LOCAL_PATH, f'myfirstvps:{SOURCE_PATH}']
    subprocess.run(command)

if __name__ == '__main__':
    main()