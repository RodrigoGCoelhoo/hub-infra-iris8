from psutil import cpu_percent, virtual_memory
from shutil import disk_usage
import mysql.connector as mysql
from datetime import datetime
import json

def sysCheck():
        
        file = open("config.json")
        data = json.load(file)

        hoje = datetime.now().isoformat(timespec='seconds')

        cpuUsage = cpu_percent(1)
        ramUsage = virtual_memory()[2]
        disk = disk_usage(r'E:\\')
        totalDisk = round(disk.total/1000000000,2)
        freeDisk = round(disk.free/1000000000,2)
        usedDisk = round(disk.used/1000000000,2)

        id_ = data["ip"]
        host = data["host"]
        user = data["user"]
        passwd = data["passwd"]
        database = data["database"]

        db = mysql.connect(
                host = host,
                user = user,
                passwd = passwd,
                database = database
                )
        
        cursor = db.cursor()

        cursor.execute(f"REPLACE INTO StatusPC VALUES ('{id_}', '{hoje}', '{cpuUsage}', '{ramUsage}', '{totalDisk}', '{freeDisk}', '{usedDisk}')")

        db.commit()

