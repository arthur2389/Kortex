from shutil import rmtree, move
from os import path
import subprocess

from KortexCore.File.File import File as File
from KortexData.KortexEnums import EFileType as EFileType


class Directory(File):

    """
    Directory object stand for one directory in Kortex project file system. Holds reference to an
    event that is placed in it. Directory is made to supply the held event the functionality of
    the file system - holding and looking up other directories and files, as well as move and
    remove procedures.
    """

    add_me = "add_directory"

    def __init__(self, name, level, dir_name=None, holding_dir=None, event=None):
        """
        Initialize Directory object
        param: name: last name of directory (str)
        param dirname: holding directory full path (str)
        param: level: directory level in project tree (int)
        param: holdingDir: Holding directory object (Directory)
        param event: event held in the directory (Event)
        """
        super(Directory, self).__init__(name=name, dir_name=dir_name, level=level, holding_dir=holding_dir)
        self._file_list = {EFileType.DIRECTORY: {},
                           EFileType.FUNCTIONAL_FILE: {}}
        self._event = event

    @property
    def functional_files(self):
        return self._file_list[EFileType.FUNCTIONAL_FILE]

    @property
    def directories(self):
        return self._file_list[EFileType.DIRECTORY]

    def add_functional_file(self, file):
        """
        Add file to the list of files that are directly under the directory
        param: file: file to add (FunctionalFile)
        """
        self._file_list[EFileType.FUNCTIONAL_FILE][file.name] = file

    def add_directory(self, file):
        """
        Add directory to the list of directories that are directly under the directory
        param: file: directory to add (Directory)
        """
        self._file_list[EFileType.DIRECTORY][file.name] = file

    def remove_functional_file(self, file):
        """
        Remove file from the list of files that are directly under the directory
        param: file: file to remove (FunctionalFile)
        """
        del self._file_list[EFileType.FUNCTIONAL_FILE][file.name]

    def remove_directory(self, file):
        """
        Remove directory from the list of directories that are directly under the directory
        param: file: directory to remove (Directory)
        """
        del self._file_list[EFileType.DIRECTORY][file.name]

    def remove(self):
        """
        Remove the current directory from the project. This will practically remove the
        event held by it.
        """
        # Remove the object from the list of directories in the holding directory
        if self._holding_dir:
            self._holding_dir.remove_directory(self)

        # Remove the directory from the file system and delete the object
        rmtree(self.path)
        del self

    def move(self, target_dir, new_name=None):
        """
        Move the current directory to a new directory in the project. This will practically move
        the event held by it to new holding event. The target directory cannot be nested in the
        moved directory
        param: targetDir: directory to move to (Directory)
        """

        # Assert that target directory is not nested inside moved directory
        found_dir = self.find_directory(target_dir.name)
        if found_dir:
            raise NotImplementedError

        # Remove the object from the list of directories in the holding directory
        if self._holding_dir:
            self._holding_dir.remove_directory(self)

        # Move the directory to new directory in file system
        move(self.path, path.join(target_dir.path, self.name))

        # Update the directory and the holding directory
        self._update_holding_directory(target_dir=target_dir)

    def open(self):
        """
        Open the directory location in file explorer
        """
        subprocess.call("explorer " + self._path)

    def copy(self, target_dir_obj=None, target_dir_path=None, new_name=None):
        """
        copy ot implemented for Directory object
        """
        raise NotImplementedError

    def find_directory(self, name, get_event=False):
        """
        Find directory by name
        param: name:  the last name of the directory (str)
        param getEvent: return the event inside the directory (bool)
        return: If found, directory (Directory) or the held event (Event), otherwise None
        """
        if self._name == name:
            return self._event if get_event else self
        for file in self._file_list[EFileType.DIRECTORY].values():
            found_obj = file.find_directory(name, get_event)
            if found_obj is not None:
                return found_obj
        return None

    def get_all_directories(self, dir_list):
        """
        Fills the given list with all the nested directories (not only the once that are directly
        held) in the directory
        param: dirList: the list to be filled with directories (list <Directory>)
        """
        for file in self._file_list[EFileType.DIRECTORY].values():
            dir_list.append(file)
            file.get_all_directories(dir_list)

    def get_event(self):
        """
        return: reference to the held event (Event)
        """
        return self._event

    def set_event(self, event):
        """
        param: event: Event to be set (Event)
        """
        self._event = event

    def __str__(self):
        """
        Debug procedure - print the directory tree
        """
        super(Directory, self).__str__()
        name = self._tabs + "<< " + self._name + " >>  "
        file_list = "["
        for _, file in self.functional_files.items():
            file_list += " " + str(file) + " "
        file_list += "]\n"
        name += file_list
        for _, _dir in self.directories.items():
            name += str(_dir)
        return name
