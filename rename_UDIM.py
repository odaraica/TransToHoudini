# coding=UTF-8
import os
import shutil


class FileRename:
    def __init__(self):
        self.allNamList = []
        self.O_N_NamDict = {}
        self.copy_success = False
        self.UDIMDict = {'_u1_v1':'_1001','_u2_v1':'_1002','_u3_v1':'_1003','_u4_v1':'_1004','_u1_v2':'_1011','_u1_v3':'_1021',\
                        '_u1_v4':'_1031','_u2_v2':'_1012'}
    def getOldNamList(self,docPath):
        if os.path.exists(docPath):
            for root,dirs,files in os.walk(docPath):
                for file in files:
                    if file.endswith('.jpg') or file.endswith('.tif') or file.endswith('.png') or file.endswith('.tiff')\
                        or file.endswith('.tga'):
                        self.allNamList.append(root + '/' + file)
        else:
            print('it is not  right TextureDocPath  please  check')
    def inputFilePath(self,filepath):
        ind = filepath.rfind('/')
        if ind>=0:
            docpath = filepath[:ind]
            #newPath = self.pathTrans(docpath)

            self.getOldNamList(docpath)
        else:
            ind1 = filepath.rfind('\\')
            if ind1>=0:
                docpath = self.pathTrans(filepath[:ind])
                self.getOldNamList(docpath)
            else:
                print('please input right filePath')


    def genNewNam(self):
        for fileNam in self.allNamList:
            for i in self.UDIMDict.keys():
                ind = fileNam.find(i)
                if ind>=0:
                    tempFileNam = fileNam[:ind] + self.UDIMDict[i] + fileNam[(ind+6):]
                    self.O_N_NamDict[fileNam] = fileNam[:ind] + '_<UDIM>' + fileNam[(ind+6):]
                    self.copyFile(fileNam,tempFileNam)
    def copyFile(self,file,newNam):
        try:
            if not os.path.exists(newNam):
                shutil.copy(file,newNam)
                self.copy_success = True
            else:
                self.copy_success = True
        except:
            print('file:{} copy error please check'.format(file))
    def pathTrans(self,oldPath):
        newPath = oldPath.replace('\\','/')
        return  newPath




