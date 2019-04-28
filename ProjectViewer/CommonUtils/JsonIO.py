import json

class JsonIO(object):

    parsedData = {}

    @staticmethod
    def CreateEmptyFile(filePath):
        with open(filePath, "w") as fileToWrite:
            json.dump({}, fileToWrite)

    @staticmethod
    def Read(filePath):
        if filePath in JsonIO.parsedData.keys():
            return JsonIO.parsedData[filePath]
        JsonIO.parsedData[filePath] = json.load(open(filePath))
        return JsonIO.parsedData[filePath]

    @staticmethod
    def Write(filePath, field, data):
        if not filePath in JsonIO.parsedData.keys():
            JsonIO.parsedData[filePath] = json.load(open(filePath))

        JsonIO.parsedData[filePath][field] = data
        with open(filePath, "w") as fileToWrite:
            json.dump(JsonIO.parsedData[filePath], fileToWrite)
        return JsonIO.parsedData[filePath]
