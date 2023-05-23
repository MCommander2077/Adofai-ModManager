import sys
import os
import json

class FileAction():
    def __init__(self):
        pass

    def loadJsonFile(self,file):
        json.load(file)
        return file

    def dumpJsonFile(self,file):
        json.dumps(file, sort_keys=True, indent=4, separators=(',', ': '))