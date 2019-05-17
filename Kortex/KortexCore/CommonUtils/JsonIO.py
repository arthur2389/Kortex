import json


class JsonIO(object):
    """
    Json operations manager. Dumps data to json files, and reads data from json files while controlling
    the read data reference the avoid multiple access to the same json file
    """

    parsedData = {}

    @staticmethod
    def CreateEmptyFile(filePath):
        """
        Create a new empty json file
        param filePath: json file full path  (str)
        """
        with open(filePath, "w") as fileToWrite:
            json.dump({}, fileToWrite)

    @staticmethod
    def Read(filePath):
        """
        Read from json file. The read data is stoted in parsedData dictionary.
        If file is already read, return the stored data from parsedData dictionary.
        param: filePath: full path to json file (str)
        """
        # If the file is already read return the content, otherwise read the file, assign
        # the content the the dictionary and return the data.
        if filePath in JsonIO.parsedData.keys():
            return JsonIO.parsedData[filePath]
        JsonIO.parsedData[filePath] = json.load(open(filePath))
        return JsonIO.parsedData[filePath]

    @staticmethod
    def Write(filePath, field, data):
        """
        Write data to json file
        param filePath: full path to data (str)
        param field: field to write (str)
        param data: data to write to the field  (str)
        """
        # Read file if it not already read
        if filePath not in JsonIO.parsedData.keys():
            JsonIO.parsedData[filePath] = json.load(open(filePath))

        # Change the field in read reference and dump the content
        JsonIO.parsedData[filePath][field] = data
        with open(filePath, "w") as fileToWrite:
            json.dump(JsonIO.parsedData[filePath], fileToWrite)
        return JsonIO.parsedData[filePath]
