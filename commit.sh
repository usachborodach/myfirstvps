#!/bin/bash
git add .
git commit
git push
ssh myfirstvps "cd myfirstvps && git pull"
ssh myfirstvps "systemctl restart timetracker"
ssh myfirstvps "systemctl status timetracker"