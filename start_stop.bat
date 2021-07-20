TIMEOUT 2
call pm2 stop horus_capture

TIMEOUT 2
call pm2 stop horus_worker

TIMEOUT 2
call pm2 stop hub_servidor

TIMEOUT 2
call pm2 start all

TIMEOUT 2



