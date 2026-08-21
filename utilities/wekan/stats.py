from sys import argv
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict
import common

if len(argv) == 1:
    argument = 30
else:
    argument = int(argv[1])

client, db = common.connect_to_mongo()
cards = db['cards']

query = {}
projection = {"createdAt": 1, "archivedAt": 1, "archived": 1, "_id": 0}
documents = cards.find(query, projection)

create_dates = list()
archive_dates = list()

for document in documents:
    if document['createdAt'] > datetime.today() - timedelta(days=argument):
        create_dates.append(document['createdAt'])
    if document['archived']:
        if document['archivedAt'] > datetime.today() - timedelta(days=argument):
            archive_dates.append(document['archivedAt'])

create_count = defaultdict(int)
for dt in create_dates:
    date_str = dt.strftime("%Y-%m-%d")
    create_count[date_str] += 1

archive_count = defaultdict(int)
for dt in archive_dates:
    date_str = dt.strftime("%Y-%m-%d")
    archive_count[date_str] += 1

all_dates = sorted(set(list(create_count.keys()) + list(archive_count.keys())))
dates = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in all_dates]
create_counts = [create_count[date_str] for date_str in all_dates]
archive_counts = [archive_count[date_str] for date_str in all_dates]

plt.figure(figsize=(12, 6))

bar_width = 0.35
x_indices = range(len(dates))

plt.bar([x - bar_width/2 for x in x_indices], create_counts, bar_width,
        label='Созданные задачи', color='skyblue', edgecolor='black', alpha=0.7)
plt.bar([x + bar_width/2 for x in x_indices], archive_counts, bar_width,
        label='Выполненные задачи', color='lightcoral', edgecolor='black', alpha=0.7)

plt.gca().set_xticks(x_indices)
plt.gca().set_xticklabels([date.strftime('%d.%m') for date in dates])
plt.gcf().autofmt_xdate()

plt.title('wekstats.py')
plt.xlabel('Дата')
plt.ylabel('Количество задач')
plt.legend()
plt.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

client.close()