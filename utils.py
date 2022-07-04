from pathlib import Path
import xml.etree.ElementTree as ET

#Define below the name of the folder containing unstacked Z images.
_RAWIMAGES="rawimages"

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

def open_XML(_file)->str:
    '''Read a RockMaker or Dragonfly XML, _file is  a file path as str, checks if Screen is
    already in database
    _screen is either a file or a screen name in ScreenFile'''
  
    if Path(_file).is_file():
        tree = ET.parse(_file)
        root = tree.getroot()
        #Create Dictionnary of localID: ingredient name    
        DictIng={}
        for chemical in root.iter('ingredients'):
            for ingredient in chemical.iter('ingredient'):
                localID=[]
                for stock in ingredient.iter('stock'):
                    DictIng[stock.find('localID').text]= {'name':str(ingredient.find('name').text),'units':str(stock.find('units').text)}
    else:
        return False

    subsections=("concentration","pH") #subsections of interest
    
    #Check number of conditions
    count=0
    for conditions in root.iter('condition'):count+=1
    if count==96: lastcol,lastrow="12","H"
    elif count==48: lastcol,lastrow="6","H"
    elif count==24: lastcol,lastrow="6","D"
    else: count=False #Plate configuration not implemented
    if count!=False:
        total_wells = [row + str(col) for row in rows if rows.index(row)<=rows.index(lastrow) 
                       for col in cols if cols.index(col)<=cols.index(lastcol)]

    i=1; my_screen={}
    for conditions in root.iter('conditions'):
        for condition in conditions.iter('condition'):
            temp=[]
            if count!=False: temp.append(total_wells[i-1])
            else:temp.append(i)
            for ingredient in condition:
                content=DictIng[ingredient.find('stockLocalID').text]['name']
                for child in ingredient:
                    # print(child.tag, child.attrib, child.text)
                    if child.tag in subsections:
                        if child.tag=='pH':
                            content+=' '+child.tag+' '+child.text
                        else:
                            content+=' '+child.text+' '+DictIng[ingredient.find('stockLocalID').text]['units']
                temp.append(content)
            my_screen[i]=temp; i+=1
        # for i,j in my_screen.items(): print(i,j)
    return my_screen
    del tree, root, DictIng
        
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
        self.rawimages=_RAWIMAGES
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
