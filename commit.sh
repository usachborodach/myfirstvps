#!/bin/bash
git add .
git commit
git push
ssh myfirstvps "cd myfirstvps && git pull"