import requests as re
import mysql.connector as mysql
import json
from datetime import datetime

def sightCheck():

    file = open("config.json")
    data = json.load(file)

    id_ = data["ip"]
    host = data["host"]
    user = data["user"]
    passwd = data["passwd"]
    database = data["database"]

    hoje = datetime.now().isoformat(timespec='seconds')

    dicInstancias = {
        "CP_15_Track_Field": "27080",
        "CP_18_Cotton": "27081",
        "CP_8_Oticas_Carol": "27082"
    }
    dicStatus = {}

    for poi, port in dicInstancias.items():
        try:
            url = f"https://localhost:{port}/JSON"
            r = re.get(url)
            content = r.text
            indexState = content.find("state")
            if content[indexState + 8] == "1":
                status = "ligado"

            elif content[indexState + 9] == "0":
                status = "desligado"
                
            else:
                status = "erro"

        except:
            status = "desligado"
            
        dicStatus[poi] = status
        
    db = mysql.connect(
            host = host,
            user = user,
            passwd = passwd,
            database = database)
        
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM StatusSightCorp WHERE id = {id_}")
    db.commit()

    for poi, status in dicStatus.items():
        db = mysql.connect(
            host = host,
            user = user,
            passwd = passwd,
            database = database)
        
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO StatusSightCorp (id, data, poi, status) VALUES ('{id_}', '{hoje}' '{poi}', '{status}')")
        db.commit()

