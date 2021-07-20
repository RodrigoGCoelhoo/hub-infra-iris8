from datetime import datetime
import os
import pickle as pk
import mysql.connector as mysql
import sys, json

class fileStatus:
    
    def __init__ (self):
        
        #self.path = path
        self.rootPath = os.getcwd()
        self.filesListPicklePath = os.path.abspath(self.rootPath + "/filesListPickle")
        self.videosPath = os.path.abspath(r"E:\\videos\\")
        self.strHoje = datetime.today().isoformat(timespec='seconds')
        self.today = datetime.today()
        self.newFileName = os.path.abspath(self.filesListPicklePath + "/" + str(self.today.year) + "_" + str(self.today.month) + "_" + str(self.today.day) + ".pickle")

        
        # Cria pasta de pickles
        if not os.path.isdir(self.filesListPicklePath):
            os.mkdir(self.filesListPicklePath)
        
        # Setups iniciais
        file = open("config.json")
        data = json.load(file)

        self.id = data["ip"]
        self.host = data["host"]
        self.user = data["user"]
        self.passwd = data["passwd"]
        self.database = data["database"]
        

    ## AUX FUNCS
    
    def oldFileList(self):
        
        filesRaw = os.listdir(self.filesListPicklePath)
        files = []
        
        for file in filesRaw:
            if file.split(".")[-1] == "pickle":
                files.append(file)

        
        if len(files) != 0:
            lastDate = datetime.strptime("2021_1_1", '%Y_%m_%d')
            for file in files:
                fileDate = datetime.strptime(file.split(".")[0], '%Y_%m_%d')
                if fileDate > lastDate and self.today.strftime('%Y_%m_%d') != fileDate.strftime('%Y_%m_%d'):
                    lastDate = fileDate

            pickleFile = self.filesListPicklePath + "/" + lastDate.strftime('%Y_%m_%d') + ".pickle"
            
            with open(os.path.abspath(self.filesListPicklePath + "/" + file), "rb") as pickleFile:
                self.lastFilesList = pk.load(pickleFile)
                        
        else:
            sys.exit(0)
            
    def coletaFilePaths(self):
        self.file_paths = os.listdir(self.videosPath)
        self.listaVideos = []
        
        for file in self.file_paths:
            if file.split(".")[-1] == "avi":
                self.listaVideos.append(file)
                
    def data_str2datetime(self, file_name):
        data_raw = file_name.split("_")[-1].split(".")[0]
        format_string = "%Y%m%d%H%M%S"
        data = datetime.strptime(data_raw, format_string)
        return data
    
    def data_mais_recente(self, data_atual, data_teste):
        if data_atual > data_teste:
            return data_atual
        else:
            return data_teste
        
    def coletaArquivosMaisRecentes(self):
        
        self.dic_arquivos_mais_recentes = {}
        
        for file in self.listaVideos:
            camera = "_".join(file.split("_")[0:3])
            
            if camera not in self.dic_arquivos_mais_recentes.keys():
                self.dic_arquivos_mais_recentes[camera] = self.data_str2datetime(file)
        
            else:
                data_atual = self.dic_arquivos_mais_recentes[camera]
                data_teste = self.data_str2datetime(file)
                data_final = self.data_mais_recente(data_atual, data_teste)
                self.dic_arquivos_mais_recentes[camera] = data_final
        
        self.arquivos_para_analisar = []
        
        for key, value in self.dic_arquivos_mais_recentes.items():
            file_sem_ext = "_".join([key,value.strftime("%Y%m%d%H%M%S")])
            fila_path = "".join([file_sem_ext, ".avi"])
            self.arquivos_para_analisar.append(fila_path)
    
    ## MAIN FUNCS
        
    def filesStatus(self):
        
        self.oldFileList()
        self.actualFilesList = os.listdir(self.videosPath)
        
        # Check deleted
        self.deleted = 0
        for file in self.lastFilesList:
            if file not in self.actualFilesList and file.split(".")[-1] == "avi":
                self.deleted += 1
                
        # Check created
        self.created = 0
        for file in self.actualFilesList:
            if file not in self.lastFilesList and file.split(".")[-1] == "avi":
                self.created += 1
    
    def createFileListPickle(self):
        
        pathNewFilesList = self.filesListPicklePath + "/" + self.today.strftime('%Y_%m_%d') + ".pickle"
        newFilesList = os.listdir(self.videosPath)
        
        with open(pathNewFilesList, "wb") as file:
            pk.dump(newFilesList, file)
            
    def coletaTamanhoFile(self):
        
        self.dic_video_size = {}
        os.chdir(self.videosPath)
        for file in self.arquivos_para_analisar:
            self.dic_video_size[file.split("_")[0]] = os.stat(file).st_size
        os.chdir(self.rootPath)
    
    def putSQLTamanhoFiles(self, poi, tamanho):
        db = mysql.connect(
        host = self.host,
        user = self.user,
        passwd = self.passwd,
        database = self.database
        )
    
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO TamanhoFiles (id, data, poi, mb) VALUES ('{self.id}', '{self.strHoje}', '{self.cleanValues(poi)}', '{round(tamanho/1000000, 0)}')")
        db.commit()
    
    def putSQLStatusFiles(self):
        db = mysql.connect(
        host = self.host,
        user = self.user,
        passwd = self.passwd,
        database = self.database
        )
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO StatusFiles (id, data, deleted, created) VALUES ('{self.id}', '{self.strHoje}', '{self.deleted}', '{self.created}')")
        db.commit()

    def cleanValues(self, value):
        v = value.replace("'","")
        v = v.replace('"','')
        return v
        
    ## Main execution
    
    def main(self):
        self.coletaFilePaths()
        self.coletaArquivosMaisRecentes()
        self.coletaTamanhoFile()

    def mainTamanho(self):
        for poi, tamanho in self.dic_video_size.items():
            self.putSQLTamanhoFiles(poi, tamanho)
    
    def mainCD(self):            
        self.filesStatus()
        self.createFileListPickle()
        self.putSQLStatusFiles()

    def run(self, boolCD = False):
        self.main()
        
        if boolCD:
            self.mainCD()
        else:
            self.mainTamanho()

p = fileStatus()
p.run()
