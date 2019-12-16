import os


#class DataDir(object):
#    def __init__(self, path):
#     self.directory = path
#     self.project = str
#     self.target = str
#     self.plate = str
#     self.date = str
#     self.prepdate = str
#     self.Directory(path)
#            
#    def Directory(self, path):
##        print("ClassPath ", path.split("/"))
#        directory = path.split("/")
#        if directory[-1]=="rawimages":
#            self.project=directory[-4]
#            self.target=directory[-4]
#            self.plate=directory[-3]
#            self.date=directory[-2].split("_")[0]
#            prep_date_path = "/".join(directory[:-2]) + "/"+ "prep_date.txt"
#        else:
#            self.project=str(directory[-3])
#            self.target=directory[-3]
#            self.plate=directory[-2]
#            self.date=directory[-1].split("_")[0]
#            prep_date_path = "/".join(directory[:-1]) + "/"+ "prep_date.txt"
#        
#        if Path(prep_date_path).exists():
#            file = open(prep_date_path)
#            contents = file.read().strip("\n")
#            self.prepdate=contents

def ensure_directory(file_path):
    """Checks the given file path for a directory, and creates one if not already present.

    Args:
        file_path: a string representing a valid URL
    """

    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
