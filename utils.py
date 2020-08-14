from pathlib import Path

# def ensure_directory(file_path):
#     """Checks the given file path for a directory, and creates one if not already present.
#     Args:
#         file_path: a string representing a valid URL
#     """

#     directory = os.path.dirname(file_path)
#     if not os.path.exists(directory):
#         os.makedirs(directory)

def ensure_directory(file_path):
    """Checks the given file path for a directory, and creates one if not already present.
    Args:
        file_path: a pathlib.Path
    """
    if not file_path.exists(): file_path.mkdir()

        
class initProject(object):
    """Initialise various variables. Put in utils for later compatibility
    if changes are needed for other microscopes.
    path is a pathlib.Path
    """
    def __init__(self, path):
        self.path=path
        self.Directory(self.path)
        
    
    def Directory(self, path):
        directory=Path.resolve(path)
        parents=directory.parents
        if directory.parts[-1]=="rawimages" or directory.parts[-1]=="cropped":
            self.rootDir = parents[1]
            self.project=directory.parts[-4]
            self.target=directory.parts[-4]
            self.plate=directory.parts[-3]
            self.date=directory.parts[-2].split("_")[0]
            self.prep_date_path = self.rootDir.joinpath("prep_date.txt")
        else:
            self.rootDir =parents[0]
            self.project=str(directory.parts[-3])
            self.target=directory.parts[-3]
            self.plate=directory.parts[-2]
            self.date=directory.parts[-1].split("_")[0]
            self.prep_date_path = self.rootDir.joinpath("prep_date.txt")
        