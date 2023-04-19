@echo off
git add .
call git commit -a -m"%COMPUTERNAME%"
call git pull 
call git push origin