def main():
    upload_csv()

def upload_csv():
    command = ['scp', 'myfirstvps', '/root/myfirstvps/utilities/reminder/reminders.csv']

if __name__ == '__main__':
    main()