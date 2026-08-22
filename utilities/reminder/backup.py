import zipfile
from datetime import date

source_file = '/root/myfirstvps/utulities/reminder/reminders.csv'
target_zip = f'/root/backups/{date.today()}_reminders.zip'
with zipfile.ZipFile(target_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(source_file, arcname='reminders.csv')
