import time
import os
import pickle as pk
import mysql.connector as mysql
import sys, json
import requests as re
from datetime import datetime
from psutil import cpu_percent, virtual_memory
from shutil import disk_usage


from sysStatus import sysCheck
from sightStatus import sightCheck
from fileStatus import fileStatus

p = fileStatus
p.run(True)

for i in range(779):
    
    sysCheck()
    #sightCheck()

    if i % 24 == 0:
        p = fileStatus
        p.run()
    
    time.sleep(60)

