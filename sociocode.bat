@echo off

set path1=\locallibrary\venv\scripts\python.exe
set path2=\locallibrary

set /p ip=Enter Ip:
set /p port=Enter Port: 

set "original_dir=%CD%"

cd /d C:\dockerdir\dockercompDB 
docker compose up -d

cd /d "%original_dir%"


echo %original_dir%%path1%

set pyPath=%original_dir%%path1%
set scriptPath=%original_dir%%path2%

set rest_command=\manage.py runserver %ip%:%port%
start chrome http://%ip%:%port%/

%pyPath% %scriptPath%%rest_command%



PAUSE
