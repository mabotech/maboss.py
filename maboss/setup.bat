
rem set CDIR = C:\MTP\mabotech\maboss1.2.2\maboss

ECHO %CD%

net stop _nginx
net stop _MaboTech_WebX
net stop _MaboTech_Scheduler
net stop _MaboTech_JobExecutor


python %CD%nginx_service.py remove
python %CD%nginx_service.py install


python %CD%mabo_serivce.py remove
python %CD%/mabo_service.py install


python %CD%/motorx/jobexecutor/mabo_service.py remove
python %CD%/motorx/jobexecutor/mabo_service.py install


python %CD%/motorx/scheduler/mabo_service.py remove
python %CD%/motorx/scheduler/mabo_service.py install

pause
