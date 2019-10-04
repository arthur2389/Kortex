from os import path, listdir, makedirs
from Kortex.KortexCore.CommonUtils.Singleton import singleton as singleton

from Kortex.KortexCore.File.Directory import Directory as Directory
from Kortex.KortexCore.File.FunctionalFile import FunctionalFile as FunctionalFile
from Kortex.KortexCore.Event.EventAdapter import EventAdapter as EventAdapter
import Kortex.KortexData.KortexEnums as KortexEnums


@singleton
class FileFactory(object):

    """
    FileFactory is used to initiate (create or map) the Kortex project file system tree. It created
    functional files, it creates and maps the directories, and gets pair Directory and Event objects
    one the another.
    """
    def __init__(self):
        self._event_adapter = EventAdapter()

    @staticmethod
    def generate_functional_file(path_file, level=0, holding_dir=None):
        """
        Create functional file object
        param: pathFile: full path to functional file (str)
        param: level: file level in project tree (int)
        param: holdingDir: holding directory object of the file (Directory)
        return: created functional file object (FunctionalFile)
        """
        assert path.isfile(path_file)
        return FunctionalFile(name=path.basename(path_file),
                              level=level,
                              holding_dir=holding_dir,
                              dir_name=path.dirname(path_file))

    def generate_directory(self, path_file, level=0, holding_dir=None):
        """
        Recursive procedure that maps directories of file system to Directory objects.
        Also creates event for each directory and maps event to it's directory.
        param: pathFile: full path to directory
        param: level: directory level in file system (int)
        param holdingDir: holding directory for the directory (Directory/None)
        return: created directory (Directory)
        """

        # Create the directory in file system if it doesn't exists
        if not path.exists(path_file):
            makedirs(path_file)

        # Create directory object, create an event and pair them
        _dir = Directory(name=path.basename(path_file),
                         dir_name=path.dirname(path_file),
                         level=level,
                         holding_dir=holding_dir)
        event = self._event_adapter.get_event(_dir, self)
        _dir.set_event(event)

        # Map all nested directories in the created directory, and remove metadata directory
        # from it as it will not be represented in the tree
        file_list = listdir(path_file)
        file_list.remove(KortexEnums.ConstantData.ProjectRepoName)

        # Go over the nested files and map them into objects (FunctionalFile/Directory)
        for file in file_list:
            full_path = path.join(path_file, file)
            if path.isdir(full_path):
                file_obj = self.generate_directory(full_path, level + 1, _dir)
                _dir.add_directory(file_obj)
            else:
                file_obj = self.generate_functional_file(full_path, level + 1, _dir)
                _dir.add_functional_file(file_obj)
        return _dir
