35 23 * * * /usr/bin/python3 /root/myfirstvps/utilities/periodic_tasks/daily.py
30 23 * * * /usr/bin/python3 /root/myfirstvps/utilities/wekan/periodic_tasks.py
14 2,8,14,20 * * * "/root/.acme.sh"/acme.sh --cron --home "/root/.acme.sh" > /dev/null
*/5 * * * * /root/myfirstvps/utilities/pull_repos/pull_repos.sh >> /var/log/sync-repos.log 2>&1
