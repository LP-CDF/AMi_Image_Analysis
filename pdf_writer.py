import fpdf
import datetime
import os
from PIL import Image


'''
Taken from
https://github.com/dakota0064/Fluorescent_Robotic_Imager
and adapted for TIFF handling by L.P.
2019
'''

class PDF(fpdf.FPDF):

    def header(self):

        # insert logo
#        self.image("util_images/logo.png", x=10, y=6, w=60, h=20)

        # position logo on the right
        #self.cell(80)

        self.set_font("Arial", size=16)

        date = datetime.date.today()
        self.cell(0, 10, str(date), align="R", ln=1)

        # set the font for the header, B=Bold
        self.set_font("Arial", style="B", size=24)

        # page title
        self.cell(0, 30, "Crystallography Report", border=0, ln=0, align="C")

        # insert a line break of 20 pixels
        self.ln(20)

    #----------------------------------------------------------------------------

    def footer(self):

        # position footer at 15mm from the bottom
        self.set_y(-15)

        # set the font, I=italic
        self.set_font("Arial", style="I", size=8)

        # display the page number and center it
        pageNum = "Page %s/{nb}" % self.page_no()
        self.cell(0, 10, pageNum, align="C")

    #-----------------------------------------------------------------------------

def create_pdf(_list):
    unsupported=[".tif",".tiff",".TIFF", ".TIF"]
    TIFFFILE=False
    name = _list[0]
    well_image = _list[1]
    project_name = _list[2]
    target_name = _list[3]
    plate_name = _list[4]
    date = _list[5]
    outputpath=_list[7]

    notes = _list[6]
#    print("TIF EXT ", os.path.splitext(os.path.basename(well_image))[1])
#    print("IMAGE PATH", well_image)
#    print("OUTPUT JPEG ", os.path.dirname(well_image)+"/"+os.path.splitext(os.path.basename(well_image))[0]+".jpeg")
    if os.path.splitext(os.path.basename(well_image))[1] in unsupported:
        img = Image.open(well_image)
        rgb_img = img.convert('RGB')
        path=os.path.dirname(well_image)+"/"+os.path.splitext(os.path.basename(well_image))[0]
        rgb_img.save(path + ".jpeg",'jpeg')
        well_image=path + ".jpeg"
        TIFFFILE=True
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("Arial", size=14)

    pdf.cell(0, 15, "Prepared by: " + name, align="C", ln=1)

    pdf.image(well_image, 30, 55, w=153, h=115)

    pdf.ln(130)

    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(50, 0, "Project name: ", align="R", ln=0)

    pdf.set_font("Arial", size=14)
    pdf.cell(0, 0, project_name, align="L", ln=1)

    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(50, 18, "Target name: ", align="R", ln=0)

    pdf.set_font("Arial", size=14)
    pdf.cell(0, 18, target_name, align="L", ln=1)

    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(50, 0, "Plate name: ", align="R", ln=0)

    pdf.set_font("Arial", size=14)
    pdf.cell(0, 0, plate_name, align="L", ln=1)

    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(50, 18, "Date of image: ", align="R", ln=0)

    pdf.set_font("Arial", size=14)
    pdf.cell(0, 18, date, align="L", ln=1)

    pdf.ln(10)

    pdf.set_font("Arial", size=14, style="B")
    pdf.cell(50, 0, "Notes: ", align="R", ln=0)

    pdf.set_font("Arial", size=14)
    pdf.cell(0, 0, notes, align="L", ln=1)

    pdf.output(outputpath)
    
    if TIFFFILE==True and os.path.exists(path + ".jpeg"):
        os.remove(path + ".jpeg")
        
