from pathlib import Path

#Define below the name of the folder containing unstacked Z images.
_rawimages="rawimages"

#Define Compatible images
Ext=[".tif",".tiff",".TIFF",".jpg", ".jpeg",".JPG",".JPEG",".png",".PNG"]

#Define rows and columns
rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

def ensure_directory(file_path):
    """Checks the given file path for a directory, and creates one if not already present.
    Args:
        file_path: a pathlib.Path
    returns the err message if permission issue, else is None
    """
    if not file_path.exists():
        try: file_path.mkdir()
        except Exception as err: return err

        
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
        self.rawimages=_rawimages
        if directory.parts[-1]==self.rawimages or directory.parts[-1]=="cropped":
            self.rootDir = parents[1]
            self.project=directory.parts[-5] #-5 if projectID is set. or -4
            self.target=directory.parts[-4]
            self.plate=directory.parts[-3]
            self.date=directory.parts[-2].split("_")[0]
            self.prep_date_path = self.rootDir.joinpath("prep_date.txt")
        else:
            self.rootDir =parents[0]
            self.project=directory.parts[-4] #-4 if projectID is set. or -3
            self.target=directory.parts[-3]
            self.plate=directory.parts[-2]
            self.date=directory.parts[-1].split("_")[0]
            self.prep_date_path = self.rootDir.joinpath("prep_date.txt")
