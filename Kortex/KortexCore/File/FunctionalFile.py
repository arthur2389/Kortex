from shutil import move, copyfile
from os import path, remove, startfile

from Kortex.KortexCore.File.File import File as File


class FuncrionalFile(File):

    """
    FunctionalFile object stand for one functional file in Kortex project file system. Functional file can
    the text, presentation, image file etc.
    """

    add_me = "add_functional_file"

    def __init__(self, name, level=0, holding_dir=None, dir_name=None):
        """
        Initialize FunctionalFile object
        param: name: last name of directory (str)
        param dirname: holding directory full path (str)
        param: level: directory level in project tree (int)
        param: holdingDir: Holding directory object (Directory)
        """
        super(FuncrionalFile, self).__init__(name=name, dir_name=dir_name, level=level, holding_dir=holding_dir)
        self._suffix = "." + name.split(".")[-1]

    @property
    def suffix(self):
        """
        Return the file suffix, that implies its functionality.
        return: fie suffix (str)
        """
        return self._suffix

    def remove(self):
        """
        Remove functional file from the Kortex project
        """

        # Update the holding directory by removing the file object
        if self._holdingDir:
            self._holdingDir.RemoveFunctionalFile(self)

        # remove file from file system and delete the object
        remove(self.path)
        del self

    def move(self, target_dir, new_name=None):
        """
        Move the current file to a new directory in the project.
        param: targetDir: directory to move to (Directory)
        """
        # Remove the object from the list of functional files in the holding directory
        if self._holdingDir:
            self._holdingDir.remove_functional_file(self)

        self._change_name_and_replace(method=move, new_name=new_name, target_dir_path=target_dir.path)

        # Update the file and the holding directory
        self._update_holding_directory(target_dir=target_dir)

    def copy(self, target_dir_obj=None, target_dir_path=None, new_name=None):
        """
        Copy functional file, possibly assign new name for it.
        param: targetDir: Full path destination for the file (str)
        param: newName: new name for the file (None/str)
        """
        if not target_dir_obj and not target_dir_path:
            raise NotImplementedError

        if target_dir_obj:
            self._change_name_and_replace(method=copyfile, new_name=new_name, target_dir_path=target_dir_obj.path)

            # Update the file and the holding directory
            self._update_holding_directory(target_dir=target_dir_obj)
        else:
            self._change_name_and_replace(method=copyfile, new_name=new_name, target_dir_path=target_dir_path)

    def open(self):
        """
        Open a functional file with it's default application
        """
        startfile(self.path)

    def _change_name_and_replace(self, method, new_name, target_dir_path):
        old_path = self.path
        if new_name:
            self.name = new_name + self._suffix
        method(old_path, path.join(target_dir_path, self.name))

    def __str__(self):
        """
        Debug procedure that prints the file name
        """
        super(FuncrionalFile, self).__str__()
        return self._name
