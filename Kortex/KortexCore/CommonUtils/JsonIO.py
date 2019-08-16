import json


class JsonIO(object):
    """
    Json operations manager. Dumps data to json files, and reads data from json files while controlling
    the read data reference the avoid multiple access to the same json file
    """

    parsed_data = {}

    @staticmethod
    def create_empty_file(file_path):
        """
        Create a new empty json file
        param filePath: json file full path  (str)
        """
        with open(file_path, "w") as fileToWrite:
            json.dump({}, fileToWrite)

    @staticmethod
    def read(file_path):
        """
        Read from json file. The read data is stoted in parsedData dictionary.
        If file is already read, return the stored data from parsedData dictionary.
        param: filePath: full path to json file (str)
        """
        # If the file is already read return the content, otherwise read the file, assign
        # the content the the dictionary and return the data.
        if file_path in JsonIO.parsed_data.keys():
            return JsonIO.parsed_data[file_path]
        JsonIO.parsed_data[file_path] = json.load(open(file_path))
        return JsonIO.parsed_data[file_path]

    @staticmethod
    def write(file_path, field, data):
        """
        Write data to json file
        param filePath: full path to data (str)
        param field: field to write (str)
        param data: data to write to the field  (str)
        """
        # Read file if it not already read
        if file_path not in JsonIO.parsed_data.keys():
            JsonIO.parsed_data[file_path] = json.load(open(file_path))

        # Change the field in read reference and dump the content
        JsonIO.parsed_data[file_path][field] = data
        with open(file_path, "w") as fileToWrite:
            json.dump(JsonIO.parsed_data[file_path], fileToWrite)
        return JsonIO.parsed_data[file_path]
