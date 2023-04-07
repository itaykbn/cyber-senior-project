@echo off

set path1=locallibrary\venv\scripts\python.exe
set path2=locallibrary

set /p ip=Enter Ip:
set /p port=Enter Port: 


set cwd=%~dp0
 
set pyPath=%cwd%%path1%
set scriptPath=%cwd%%path2%

set rest_command=\manage.py runserver %ip%:%port%
start chrome http://%ip%:%port%/

%pyPath% %scriptPath%%rest_command%



PAUSE
